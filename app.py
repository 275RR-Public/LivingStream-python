import cv2

from lib.tracker import Tracker
from lib.ui import UI
from lib.network import Network
from lib.calibration import generate_aruco_markers, calibrate

# Initialize components
tracker = Tracker()     # person detection and tracking
ui = UI()               # UI using openCV
network = Network()     # send tracking data to Unity

# Main application loop
while True:
    current_mode = ui.get_mode()

    if current_mode == "home":
        frame = ui.create_home_screen()
        cv2.imshow(ui.window_name, frame)

    elif current_mode == "config":
        frame = ui.create_config_screen()
        cv2.imshow(ui.window_name, frame)
        # Handle marker creation request
        if ui.create_markers_requested:
            generate_aruco_markers(cv2.aruco.DICT_6X6_250, [0, 1, 2], 200, "markers")
            ui.create_markers_requested = False
            print("Markers created in 'markers' directory.")
        # Handle calibration request
        if ui.calibrate_requested:
            tracker.stop()  # Stop the RealSense pipeline
            marker_to_unity = {0: [0.0, 0.0, 0.0], 1: [1.0, 0.0, 0.0], 2: [0.0, 0.0, 1.0]}
            calibrate(cv2.aruco.DICT_6X6_250, marker_to_unity)
            tracker.start_pipeline()  # Restart the pipeline
            ui.calibrate_requested = False
            print("Calibration ended.")

    elif current_mode == "testing":
        tracking_data, color_image, depth_colormap, total_delay = tracker.process_frame(with_images=True)
        if color_image is not None:
            ui.display_tracking_frame(color_image, depth_colormap, tracking_data)
        network.send_tracking_data(tracking_data)

    elif current_mode == "live":
        tracking_data, _, _, total_delay = tracker.process_frame(with_images=False)
        frame = ui.create_live_screen(tracker.model.device, total_delay)
        cv2.imshow(ui.window_name, frame)
        network.send_tracking_data(tracking_data)

    elif current_mode == "exit":
        break

    # Handle keyboard input - "q" for back/exit
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        ui.set_mode("home" if current_mode != "home" else "exit")

# Cleanup
tracker.stop()
network.close()
cv2.destroyAllWindows()