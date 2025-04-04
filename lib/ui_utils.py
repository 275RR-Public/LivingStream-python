import cv2
import ctypes
from .ui_settings import DEFAULT_WIDTH, DEFAULT_HEIGHT, BUTTON_SIZE, TEXT_SETTINGS

class UIUtils:
    def __init__(self):
        # Use global settings
        self.default_width = DEFAULT_WIDTH
        self.default_height = DEFAULT_HEIGHT
        self.button_size = BUTTON_SIZE
        self.text_settings = TEXT_SETTINGS

        # Get screen resolution on Windows
        def get_screen_resolution():
            user32 = ctypes.windll.user32
            return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

        monitor_width, monitor_height = get_screen_resolution()
        print(f"Screen resolution: {monitor_width}x{monitor_height}")

        # Adjust window resolution to fit monitor while maintaining aspect ratio
        aspect_ratio = self.default_width / self.default_height
        if self.default_width > monitor_width or self.default_height > monitor_height:
            if monitor_width / aspect_ratio <= monitor_height:
                self.window_width = monitor_width
                self.window_height = int(monitor_width / aspect_ratio)
            else:
                self.window_height = monitor_height
                self.window_width = int(monitor_height * aspect_ratio)
        else:
            self.window_width = self.default_width
            self.window_height = self.default_height

        # Scaling factors relative to default resolution
        self.scale_x = self.window_width / self.default_width
        self.scale_y = self.window_height / self.default_height

    def scale_point(self, x, y):
        """Scale a point (x, y) based on the window resolution."""
        return int(x * self.scale_x), int(y * self.scale_y)

    def scale_size(self, width, height):
        """Scale a size (width, height) based on the window resolution."""
        return int(width * self.scale_x), int(height * self.scale_y)

    def scale_value(self, value, axis='x'):
        """Scale a single value (e.g., font size, thickness) based on the axis."""
        return int(value * (self.scale_x if axis == 'x' else self.scale_y))

    def get_text_width(self, text, font_scale, thickness):
        """Calculate the width of text in pixels."""
        font = cv2.FONT_HERSHEY_SIMPLEX
        (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)
        return text_width

    def center_x(self, object_width):
        """Calculate the x-coordinate to center an object of given width."""
        return (self.window_width - object_width) // 2

    def get_window_size(self):
        """Return the adjusted window size."""
        return self.window_width, self.window_height

    def get_scaled_button_size(self):
        """Return the scaled button size."""
        return self.scale_size(*self.button_size)

    def get_scaled_text_properties(self, text_type):
        """Return the scaled font scale and thickness for the given text type."""
        font_scale = self.text_settings[text_type]["font_scale"]
        thickness = self.text_settings[text_type]["thickness"]
        scaled_font_scale = self.scale_value(font_scale, 'y')
        scaled_thickness = self.scale_value(thickness, 'y')
        # Ensure font scale and thickness are not too small
        scaled_font_scale = max(scaled_font_scale, 0.5)  # Minimum font scale
        scaled_thickness = max(scaled_thickness, 1)  # Minimum thickness
        return scaled_font_scale, scaled_thickness