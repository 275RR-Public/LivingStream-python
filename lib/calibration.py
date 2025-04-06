import cv2
import numpy as np
import pyrealsense2 as rs
import os

def generate_aruco_markers(dictionary_type, marker_ids, image_size, output_dir):
    """
    Generate ArUco marker images and save them to the specified directory.

    Parameters:
    - dictionary_type: int, the predefined ArUco dictionary (e.g., cv2.aruco.DICT_6X6_250)
    - marker_ids: list of int, the IDs of the markers to generate
    - image_size: int, the size of the marker image in pixels (width and height)
    - output_dir: str, the directory where the marker images will be saved
    """
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Initialize the ArUco dictionary
    dictionary = cv2.aruco.getPredefinedDictionary(dictionary_type)
    
    # Generate and save each marker
    for marker_id in marker_ids:
        marker_img = cv2.aruco.generateImageMarker(dictionary, marker_id, image_size)
        cv2.imwrite(os.path.join(output_dir, f"marker_{marker_id}.png"), marker_img)
    
    print(f"Generated {len(marker_ids)} ArUco markers in {output_dir}")

def setup_realsense():
    """
    Initialize and start the RealSense pipeline for color and depth streams.

    Returns:
    - pipeline: the RealSense pipeline object
    - align: the alignment object to align depth to color
    - intrinsics: the color camera intrinsics
    """
    pipeline = rs.pipeline()
    config = rs.config()
    
    # Enable depth and color streams
    config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
    
    # Start the pipeline
    pipeline.start(config)
    
    # Set up alignment of depth to color
    align = rs.align(rs.stream.color)
    
    # Get color camera intrinsics
    profile = pipeline.get_active_profile()
    color_profile = rs.video_stream_profile(profile.get_stream(rs.stream.color))
    intrinsics = color_profile.get_intrinsics()
    
    return pipeline, align, intrinsics

def detect_aruco_markers(color_image, dictionary):
    """
    Detect ArUco markers in the provided color image.

    Parameters:
    - color_image: numpy array, the BGR image from the RealSense color stream
    - dictionary: the ArUco dictionary object

    Returns:
    - marker_corners: list of detected marker corners
    - marker_ids: list of detected marker IDs
    """
    parameters = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(dictionary, parameters)
    marker_corners, marker_ids, _ = detector.detectMarkers(color_image)
    
    # Handle case where no markers are detected
    if marker_ids is None:
        marker_ids = []
    
    return marker_corners, marker_ids

def get_marker_3d_positions(marker_corners, depth_frame, intrinsics):
    """
    Compute the 3D positions of detected markers using the depth frame.

    Parameters:
    - marker_corners: list of marker corners from detect_aruco_markers
    - depth_frame: RealSense depth frame object
    - intrinsics: color camera intrinsics

    Returns:
    - positions: list of 3D points (or None if depth is invalid) for each marker's center
    """
    positions = []
    for corners in marker_corners:
        # Calculate the center of the marker
        center_x = int(np.mean([c[0][0] for c in corners]))
        center_y = int(np.mean([c[0][1] for c in corners]))
        
        # Get depth at the center
        depth = depth_frame.get_distance(center_x, center_y)
        
        if depth > 0:
            # Convert pixel coordinates and depth to 3D point
            point_3d = rs.rs2_deproject_pixel_to_point(intrinsics, [center_x, center_y], depth)
            positions.append(point_3d)
        else:
            positions.append(None)  # Invalid depth reading
    
    return positions

def compute_transformation(P_camera, P_unity):
    """
    Compute the scale, rotation, and translation to map camera coordinates to Unity coordinates.

    Parameters:
    - P_camera: list of 3D points in camera coordinate system
    - P_unity: list of corresponding 3D points in Unity coordinate system

    Returns:
    - s: float, scale factor
    - R: 3x3 numpy array, rotation matrix
    - t: 3x1 numpy array, translation vector
    """
    P_camera = np.array(P_camera)
    P_unity = np.array(P_unity)
    
    # Center the point sets
    centroid_camera = np.mean(P_camera, axis=0)
    centroid_unity = np.mean(P_unity, axis=0)
    P_camera_centered = P_camera - centroid_camera
    P_unity_centered = P_unity - centroid_unity
    
    # Compute scale factor
    s = np.linalg.norm(P_unity_centered) / np.linalg.norm(P_camera_centered)
    
    # Compute rotation using SVD
    H = P_camera_centered.T @ P_unity_centered
    U, _, Vt = np.linalg.svd(H)
    R = Vt.T @ U.T
    
    # Ensure a proper rotation matrix (determinant = 1)
    if np.linalg.det(R) < 0:
        Vt[-1, :] *= -1
        R = Vt.T @ U.T
    
    # Compute translation
    t = centroid_unity - s * (R @ centroid_camera)
    
    return s, R, t

def save_transformation(scale, rotation, translation, filename="calibration_config.py"):
    """
    Save the transformation parameters to a Python file for later use.

    Parameters:
    - scale: float, scale factor
    - rotation: 3x3 numpy array, rotation matrix
    - translation: 3x1 numpy array, translation vector
    - filename: str, the file to save the parameters (default: 'calibration_config.py')
    """
    # Determine the directory where the script is located (the 'lib' folder)
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Path to 'lib'
    transform_file = os.path.join(script_dir, filename)      # Full path to save file

    with open(transform_file, 'w') as f:
        f.write("import numpy as np\n\n")  # Add NumPy import for the config file
        f.write(f"SCALE = {scale}\n")
        f.write(f"ROTATION_MATRIX = np.array({rotation.tolist()})\n")
        f.write(f"TRANSLATION_VECTOR = np.array({translation.tolist()})\n")
    print(f"Transformation saved to {transform_file}")

def calibrate(dictionary_type, marker_to_unity, output_file="calibration_config.py"):
    """
    Perform calibration using ArUco markers to align camera coordinates with Unity coordinates.

    Parameters:
    - dictionary_type: int, the ArUco dictionary type (e.g., cv2.aruco.DICT_6X6_250)
    - marker_to_unity: dict, mapping marker IDs to their known Unity 3D positions (e.g., {0: [0,0,0]})
    - output_file: str, file to save the transformation parameters
    """
    # Initialize RealSense pipeline
    pipeline, align, intrinsics = setup_realsense()
    
    try:
        # step 1 - Prompt user to measure the real-world distance between green and red circles
        # This step is needed to scale the Unity world to the projector's scale on the floor
        #print("STEP 1. Measure the actual distance (in meters) between the centers of the green and red circles on the floor.")
        #real_world_distance = float(input("Enter the distance in meters (e.g., 0.743) then press Enter: "))
        
        # Define the Unity distance between green and red circles (assumed to be 1 meter)
        #unity_distance = 1.0  # Assuming green is at (0,0,0) and red is at (1,0,0) in Unity
        #projection_scale = real_world_distance / unity_distance
        
        # step 2 - map into Unity
        print("Place all the ArUco markers then press Enter when ready...")
        input()  # Wait for user confirmation
        
        # Capture and align frames
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)
        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())
        
        # Detect ArUco markers
        dictionary = cv2.aruco.getPredefinedDictionary(dictionary_type)
        marker_corners, marker_ids = detect_aruco_markers(color_image, dictionary)
        
        # Check if enough markers are detected
        if len(marker_ids) < 3:
            print("Error: Less than 3 markers detected. Calibration aborted.")
            return
        
        # Compute 3D positions of detected markers
        positions = get_marker_3d_positions(marker_corners, depth_frame, intrinsics)
        
        # Match detected markers to known Unity positions
        P_camera = []
        P_unity = []
        for i, marker_id in enumerate(marker_ids):
            marker_id = marker_id[0]  # marker_ids is a list of arrays
            if marker_id in marker_to_unity and positions[i] is not None:
                P_camera.append(positions[i])
                P_unity.append(marker_to_unity[marker_id])
        
        # Ensure enough valid points for transformation
        if len(P_camera) < 3:
            print("Error: Less than 3 valid markers with known Unity positions.")
            return
        
        # Compute the transformation
        s, R, t = compute_transformation(P_camera, P_unity)
        
        # Part of step 1
        # Adjust the scale factor by dividing by the projection scale
        #adjusted_scale = s / projection_scale
        
        # Save the adjusted transformation parameters
        save_transformation(s, R, t, output_file)
    
    finally:
        # Ensure the pipeline is stopped even if an error occurs
        pipeline.stop()