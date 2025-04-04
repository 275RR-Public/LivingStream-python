import cv2
import numpy as np
from .ui_utils import UIUtils
from .ui_elements import UIElements
from .ui_settings import DEFAULT_HEIGHT

class UI:
    def __init__(self):
        # Initialize UI utilities and elements
        self.ui_utils = UIUtils()
        self.ui_elements = UIElements(self.ui_utils)

        # Get window size from UIUtils
        self.window_width, self.window_height = self.ui_utils.get_window_size()

        # Initialize window
        self.window_name = "LivingStream Object Tracking"
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window_name, self.window_width, self.window_height)
        cv2.setMouseCallback(self.window_name, self.ui_elements.mouse_callback)

        self.mode = "home"
        # Flags to signal config actions
        self.calibrate_requested = False
        self.create_markers_requested = False

    def create_home_screen(self):
        """Create the home screen with centered elements."""
        frame = np.full((self.window_height, self.window_width, 3), (100, 100, 100), dtype=np.uint8)

        # Clear previous buttons
        self.ui_elements.clear_buttons()

        # Title (centered horizontally, 250 pixels from top)
        self.ui_elements.create_title_text(frame, "Detection and Tracking", (0, 0, 0),
                                           (None, self.ui_utils.scale_point(0, 200)[1]))

        # Buttons (centered horizontally, stacked vertically with padding)
        btn_width, _ = self.ui_utils.get_scaled_button_size()
        btn_center_x = self.ui_utils.center_x(btn_width)
        padding = self.ui_elements.get_scaled_padding()

        # Test Mode button
        test_btn_y = self.ui_utils.scale_point(0, 350)[1]
        self.ui_elements.create_button(
            frame, "test", "Test Mode", (255, 255, 255), (btn_center_x, test_btn_y),
            lambda: self.set_mode("testing")
        )

        # Config button
        config_btn_y = test_btn_y + self.ui_utils.get_scaled_button_size()[1] + padding
        self.ui_elements.create_button(
            frame, "config", "Config Mode", (255, 255, 255), (btn_center_x, config_btn_y),
            lambda: self.set_mode("config")
        )

        # Live Mode button
        live_btn_y = config_btn_y + self.ui_utils.get_scaled_button_size()[1] + padding
        self.ui_elements.create_button(
            frame, "live", "Live Mode", (0, 255, 0), (btn_center_x, live_btn_y),
            lambda: self.set_mode("live")
        )

        # Exit button
        exit_btn_y = live_btn_y + self.ui_utils.get_scaled_button_size()[1] + padding
        self.ui_elements.create_button(
            frame, "exit", "Exit", (255, 255, 255), (btn_center_x, exit_btn_y),
            lambda: self.set_mode("exit")
        )

        return frame

    def create_config_screen(self):
        """Create the configuration screen with options for markers and calibration."""
        frame = np.full((self.window_height, self.window_width, 3), (100, 100, 100), dtype=np.uint8)

        # Clear previous buttons
        self.ui_elements.clear_buttons()

        # Title
        self.ui_elements.create_title_text(frame, "Configuration", (0, 0, 0),
                                           (None, self.ui_utils.scale_point(0, 200)[1]))

        # Buttons
        btn_width, _ = self.ui_utils.get_scaled_button_size()
        btn_center_x = self.ui_utils.center_x(btn_width)
        padding = self.ui_elements.get_scaled_padding()

        # Create Markers button
        create_markers_btn_y = self.ui_utils.scale_point(0, 350)[1]
        self.ui_elements.create_button(
            frame, "create_markers", "Create Markers", (255, 255, 255), (btn_center_x, create_markers_btn_y),
            lambda: setattr(self, 'create_markers_requested', True)
        )

        # Calibrate button
        calibrate_btn_y = create_markers_btn_y + self.ui_utils.get_scaled_button_size()[1] + padding
        self.ui_elements.create_button(
            frame, "calibrate", "Calibrate", (255, 255, 255), (btn_center_x, calibrate_btn_y),
            lambda: setattr(self, 'calibrate_requested', True)
        )

        # Back button
        back_btn_y = calibrate_btn_y + self.ui_utils.get_scaled_button_size()[1] + padding
        self.ui_elements.create_button(
            frame, "back", "Back", (255, 255, 255), (btn_center_x, back_btn_y),
            lambda: self.set_mode("home")
        )

        return frame

    def create_live_screen(self, device, total_delay):
        """Create the live screen with centered elements."""
        frame = np.full((self.window_height, self.window_width, 3), (100, 100, 100), dtype=np.uint8)

        # Clear previous buttons
        self.ui_elements.clear_buttons()

        # Text (centered vertically and horizontally)
        self.ui_elements.create_title_text(frame, "Sending data to Unity...", (0, 0, 0),
                                           (None, self.ui_utils.scale_point(0, 200)[1]))
        self.ui_elements.create_title_text(frame, f"AI using {device} with delay of {total_delay:.1f}ms",
                                           (0, 0, 0), (None, self.ui_utils.scale_point(0, 300)[1]))

        # Back button
        btn_width, _ = self.ui_utils.get_scaled_button_size()
        btn_center_x = self.ui_utils.center_x(btn_width)
        back_btn_y = self.ui_utils.scale_point(0, DEFAULT_HEIGHT - 50)[1]
        self.ui_elements.create_button(
            frame, "back", "Back", (255, 255, 255), (btn_center_x, back_btn_y),
            lambda: self.set_mode("home")
        )

        return frame

    def display_tracking_frame(self, color_image, depth_colormap, tracking_data):
        """Draw tracking info on color_image and display with depth_colormap."""
        color_image_resized = cv2.resize(color_image, (self.window_width // 2, self.window_height))
        depth_colormap_resized = cv2.resize(depth_colormap, (self.window_width // 2, self.window_height))

        for track in tracking_data:
            x_min, y_min, x_max, y_max = track['bbox']
            track_id = track['id']
            position = track['position']

            scale_x = (self.window_width // 2) / color_image.shape[1]
            scale_y = self.window_height / color_image.shape[0]
            x_min, y_min = int(x_min * scale_x), int(y_min * scale_y)
            x_max, y_max = int(x_max * scale_x), int(y_max * scale_y)

            feet_pixel = (x_min + (x_max - x_min) // 2, y_max)

            if position is not None:
                pos_x, pos_y, depth = position[0], position[1], position[2]
                cv2.rectangle(color_image_resized, (x_min, y_min), (x_max, y_max), (0, 255, 0), self.ui_utils.scale_value(2, 'x'))
                cv2.circle(color_image_resized, feet_pixel, self.ui_utils.scale_value(6, 'x'), (0, 0, 255), -1)
                self.ui_elements.create_note_text(color_image_resized, f"ID: {track_id}", (0, 255, 0),
                                                  (x_min + self.ui_utils.scale_value(5, 'x'), y_min + self.ui_utils.scale_value(20, 'y')))
                self.ui_elements.create_note_text(color_image_resized, f"X: {pos_x:.2f}, Y: {pos_y:.2f}", (0, 255, 0),
                                                  (x_min + self.ui_utils.scale_value(5, 'x'), y_min + self.ui_utils.scale_value(50, 'y')))
                self.ui_elements.create_note_text(color_image_resized, f"Depth: {depth:.2f}m", (0, 255, 0),
                                                  (x_min + self.ui_utils.scale_value(5, 'x'), y_min + self.ui_utils.scale_value(80, 'y')))
            else:
                cv2.rectangle(color_image_resized, (x_min, y_min), (x_max, y_max), (0, 0, 255), self.ui_utils.scale_value(2, 'x'))
                self.ui_elements.create_note_text(color_image_resized, f"ID: {track_id}", (0, 0, 255),
                                                  (x_min + self.ui_utils.scale_value(5, 'x'), y_min + self.ui_utils.scale_value(20, 'y')))
                self.ui_elements.create_note_text(color_image_resized, "No depth", (0, 0, 255),
                                                  (x_min + self.ui_utils.scale_value(5, 'x'), y_min + self.ui_utils.scale_value(50, 'y')))

        display_image = np.hstack((color_image_resized, depth_colormap_resized))
        self.ui_elements.clear_buttons()

        btn_width, _ = self.ui_utils.get_scaled_button_size()
        btn_center_x = self.ui_utils.center_x(btn_width)
        back_btn_y = self.ui_utils.scale_point(0, DEFAULT_HEIGHT - 50)[1]
        self.ui_elements.create_button(
            display_image, "back", "Back", (255, 255, 255), (btn_center_x, back_btn_y),
            lambda: self.set_mode("home")
        )

        cv2.imshow(self.window_name, display_image)

    def get_mode(self):
        return self.mode

    def set_mode(self, new_mode):
        self.mode = new_mode