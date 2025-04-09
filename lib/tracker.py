import importlib
import numpy as np
import pyrealsense2 as rs                       # python wrapper of d435i SDK
from ultralytics import YOLO                    # AI for object detect, track, and pose
import torch                                    # For CUDA detection

class Tracker:
    def __init__(self, force_cpu=False):
        self.intrinsics = None                  # Will store camera intrinsics
        self.pipeline = rs.pipeline()           # Initialize and start RealSense pipeline
        self.config = rs.config()
        self.config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)   # up to 1280x720
        self.config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)  # up to 1920x1080
        #self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 15)
        #self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 15)
        self.profile = self.pipeline.start(self.config)

        self.align = rs.align(rs.stream.color)  # Aligns depth to color
        self.colorizer = rs.colorizer()         # Create colorizer for depth visualization

        if not force_cpu and torch.cuda.is_available():     # Check for CUDA availability
            self.device = 'cuda'
        else:
            self.device = 'cpu'                             # Fallback to CPU

        self.model = YOLO('yolo11n-pose.pt').to(self.device)

        self.person_class = 0                   # YOLO - Class 0 is 'person'
        self.person_confidence = 0.6            # YOLO - Percent confident of detection
        self.feet_confidence = 0.6              # YOLO - Percent confident of keypoint
        self.max_tracks = 3                     # Maximum number of people to track
        self.active_tracks = set()              # Keep track of currently active track IDs

        # Region of Interest (ROI)
        self.roi_min_depth = 1                  # min valid depth range (in meters)
        self.roi_max_depth = 4                  # max valid depth range (in meters)
        self.roi_size = 5                       # Half-size for a 10x10 pixel ROI around feet for depth sampling
        self.roi_depth_history = {}             # for smoothing (stores depth values for each track, now single EMA value)

        # Get depth scale for converting depth frame to meters
        depth_sensor = self.profile.get_device().first_depth_sensor()
        self.depth_scale = depth_sensor.get_depth_scale()  # Typically 0.001 for D435i

        # Load calibration parameters initially
        self.load_calibration()

    def load_calibration(self):
        """
        Load or reload transformation parameters from calibration_config.py.
        """
        try:
            # Import the module relative to the 'lib' package
            calibration_config = importlib.import_module('.calibration_config', package='lib')
            # Reload to ensure the latest file contents are used
            importlib.reload(calibration_config)
            self.scale = calibration_config.SCALE
            self.rotation_matrix = calibration_config.ROTATION_MATRIX
            self.translation_vector = calibration_config.TRANSLATION_VECTOR
            print("Loaded transformation: calibration_config.py")
        except ImportError:
            print("calibration_config.py not found. Using default transformation.")
            self.scale = 1.0
            self.rotation_matrix = np.eye(3)
            self.translation_vector = np.zeros(3)

    def process_frame(self, with_images=False):
        """Process a frame and return tracking data, optionally with images."""
        # Get frames and convert to numpy array
        frames = self.pipeline.wait_for_frames()
        aligned_frames = self.align.process(frames)
        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        if not depth_frame or not color_frame:
            return [], None, None, 0 if with_images else []
        
        # Get camera intrinsics from the color frame (only once)
        if self.intrinsics is None:
            color_profile = color_frame.profile.as_video_stream_profile()
            self.intrinsics = color_profile.intrinsics

        color_image = np.asanyarray(color_frame.get_data())

        # Convert depth frame to meters once per frame for efficient ROI sampling
        depth_image = np.asanyarray(depth_frame.get_data(), dtype=np.float32) * self.depth_scale

        # Detection and tracking with YOLO pose model
        # persist=True enables tracking; add half=True for FP16 if desired
        results = self.model.track(color_image, persist=True)
        tracking_data = []

        # Limit the number of simultaneous tracks to process
        # Step 1. Collect all valid detections with track IDs
        current_detections = {}
        if results[0].boxes is not None:
            for i in range(len(results[0].boxes)):
                # Check all conditions using indexed tensor access
                # SKIP if no track ID, low confidence, or not a person
                if (results[0].boxes.id is not None and
                        results[0].boxes.conf[i] >= self.person_confidence and
                        int(results[0].boxes.cls[i]) == self.person_class):
                    track_id = int(results[0].boxes.id[i])
                    current_detections[track_id] = i

        # Step 2. Update active tracks and Remove tracks that are no longer detected
        self.active_tracks = {track_id for track_id in self.active_tracks if track_id in current_detections}
    
        # Step 3. Add new tracks if we have space
        for track_id in current_detections:
            if len(self.active_tracks) < self.max_tracks and track_id not in self.active_tracks:
                self.active_tracks.add(track_id)
                if len(self.active_tracks) == self.max_tracks:
                    break

        # Step 4: Process only the max active tracks
        for track_id in self.active_tracks:
            if track_id not in current_detections:
                continue  # Skip if the track is not detected in this frame
            i = current_detections[track_id]

            # Keep bbox on GPU, extract scalars with .item()
            bbox = results[0].boxes.xyxy[i]  # [x_min, y_min, x_max, y_max] as tensor
            x_min = max(0, int(bbox[0].item()))
            y_min = max(0, int(bbox[1].item()))
            x_max = min(color_frame.get_width() - 1, int(bbox[2].item()))
            y_max = min(color_frame.get_height() - 1, int(bbox[3].item()))

            # Skip if bounding box is too small
            if x_max - x_min < 10 or y_max - y_min < 10:
                continue

            # Keep keypoints on GPU, extract only ankle data
            kpts = results[0].keypoints.data[i]  # [17, 3] for x, y, confidence as tensor
            if kpts.shape != (17, 3):
                continue  # Ensure key points array is valid

            # Extract feet position from key points (COCO: 15 = left ankle, 16 = right ankle)
            left_ankle_x = kpts[15, 0].item()  # [x, y, conf]
            left_ankle_y = kpts[15, 1].item()
            left_ankle_conf = kpts[15, 2].item()
            right_ankle_x = kpts[16, 0].item()
            right_ankle_y = kpts[16, 1].item()
            right_ankle_conf = kpts[16, 2].item()

            # Determine midpoint based on available feet position
            if left_ankle_conf > self.feet_confidence and right_ankle_conf > self.feet_confidence:
                feet_x = (left_ankle_x + right_ankle_x) / 2
                feet_y = (left_ankle_y + right_ankle_y) / 2
            elif left_ankle_conf > self.feet_confidence:
                feet_x, feet_y = left_ankle_x, left_ankle_y
            elif right_ankle_conf > self.feet_confidence:
                feet_x, feet_y = right_ankle_x, right_ankle_y
            else:
                # Fallback: use bottom center of bounding box
                feet_x = x_min + (x_max - x_min) / 2
                feet_y = y_max

            # Vectorized depth sampling in ROI using NumPy slicing
            x_center = int(feet_x)
            y_center = int(feet_y)
            x_start = max(0, x_center - self.roi_size)
            x_end = min(depth_frame.get_width(), x_center + self.roi_size + 1)
            y_start = max(0, y_center - self.roi_size)
            y_end = min(depth_frame.get_height(), y_center + self.roi_size + 1)
            roi_depths = depth_image[y_start:y_end, x_start:x_end]
            valid_depths = roi_depths[(roi_depths > self.roi_min_depth) & (roi_depths < self.roi_max_depth)]

            depth = None
            if valid_depths.size > 0:
                current_depth = np.median(valid_depths)
                # Use exponential moving average (EMA) for smoothing instead of list-based median
                alpha = 0.2  # Smoothing factor
                if track_id not in self.roi_depth_history:
                    self.roi_depth_history[track_id] = current_depth
                else:
                    self.roi_depth_history[track_id] = alpha * current_depth + (1 - alpha) * self.roi_depth_history[track_id]
                depth = self.roi_depth_history[track_id]
            else:
                print(f"Track ID {track_id}: No valid depths at ({feet_x}, {feet_y})")

            # Deproject to 3D with transformation if depth is valid
            point_3d = None
            if depth is not None:
                # Get 3D point in camera coordinate frame
                point_3d_camera = rs.rs2_deproject_pixel_to_point(self.intrinsics, [feet_x, feet_y], depth)
                # Apply transformation for Unity frame: scale, rotate, translate
                point_3d_transformed = self.scale * (self.rotation_matrix @ point_3d_camera) + self.translation_vector
                point_3d = point_3d_transformed.tolist()
            
            # Add to tracking data
            tracking_data.append({
                'id': track_id,
                'position': point_3d if point_3d else None,
                'bbox': [x_min, y_min, x_max, y_max]
            })

        # Clean up depth history for tracks that are no longer active
        self.roi_depth_history = {k: v for k, v in self.roi_depth_history.items() if k in self.active_tracks}

        # Extract timing information
        preprocess_time = results[0].speed['preprocess']
        inference_time = results[0].speed['inference']
        postprocess_time = results[0].speed['postprocess']
        total_delay = preprocess_time + inference_time + postprocess_time

        # if testing mode, send images
        if with_images:
            # Create depth colormap for visualization
            depth_colormap = np.asanyarray(self.colorizer.colorize(depth_frame).get_data())
            return tracking_data, color_image, depth_colormap, total_delay
        return tracking_data, None, None, total_delay

    def stop(self):
        self.pipeline.stop()

    def start_pipeline(self):
        """ReStart the RealSense pipeline after config"""
        self.pipeline.start(self.config)