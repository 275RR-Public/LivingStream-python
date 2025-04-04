import cv2
from .ui_settings import BUTTON_SIZE, BUTTON_BG_COLOR, PADDING, TEXT_SETTINGS

class UIElements:
    def __init__(self, ui_utils):
        self.ui_utils = ui_utils
        self.button_size = BUTTON_SIZE
        self.button_bg_color = BUTTON_BG_COLOR
        self.padding = PADDING
        self.text_settings = TEXT_SETTINGS

        # Store buttons and their actions
        self.buttons = {}  # {button_id: (bounds, action)}

    def create_button(self, frame, button_id, text, font_color, top_left, action):
        """Create a button on the frame at the specified top-left position."""
        btn_width, btn_height = self.ui_utils.get_scaled_button_size()
        btn_x1, btn_y1 = top_left
        btn_x2, btn_y2 = btn_x1 + btn_width, btn_y1 + btn_height

        # Draw button rectangle
        cv2.rectangle(frame, (btn_x1, btn_y1), (btn_x2, btn_y2), self.button_bg_color, -1)

        # Draw button text
        text_font_scale, text_thickness = self.ui_utils.get_scaled_text_properties("button")
        text_width = self.ui_utils.get_text_width(text, text_font_scale, text_thickness)
        text_x = btn_x1 + (btn_width - text_width) // 2
        text_y = btn_y1 + (btn_height + self.ui_utils.scale_value(20, 'y')) // 2
        cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX,
                    text_font_scale, font_color, text_thickness)

        # Store button bounds and action
        self.buttons[button_id] = ((btn_x1, btn_y1, btn_x2, btn_y2), action)
        return (btn_x1, btn_y1, btn_x2, btn_y2)

    def create_title_text(self, frame, text, font_color, top_left):
        """Create title text on the frame at the specified top-left position."""
        text_font_scale, text_thickness = self.ui_utils.get_scaled_text_properties("title")
        text_width = self.ui_utils.get_text_width(text, text_font_scale, text_thickness)
        text_x = self.ui_utils.center_x(text_width) if top_left[0] is None else top_left[0]
        text_y = top_left[1]
        cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX,
                    text_font_scale, font_color, text_thickness)
        return (text_x, text_y, text_x + text_width, text_y + self.ui_utils.scale_value(40, 'y'))

    def create_note_text(self, frame, text, font_color, top_left):
        """Create note text (e.g., tracking info) on the frame at the specified top-left position."""
        text_font_scale, text_thickness = self.ui_utils.get_scaled_text_properties("tracking")
        text_width = self.ui_utils.get_text_width(text, text_font_scale, text_thickness)
        text_x = top_left[0]
        text_y = top_left[1]

        # Ensure text is within the frame
        if text_y < 0:
            text_y = self.ui_utils.scale_value(20, 'y')  # Move text down to a visible position
        if text_x < 0:
            text_x = 0
        if text_x + text_width > frame.shape[1]:
            text_x = frame.shape[1] - text_width - self.ui_utils.scale_value(5, 'x')
        if text_y > frame.shape[0]:
            text_y = frame.shape[0] - self.ui_utils.scale_value(20, 'y')

        cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX,
                    text_font_scale, font_color, text_thickness)
        return (text_x, text_y, text_x + text_width, text_y + self.ui_utils.scale_value(20, 'y'))

    def get_scaled_padding(self):
        """Return the scaled padding value."""
        return self.ui_utils.scale_value(self.padding, 'y')

    def mouse_callback(self, event, x, y, flags, param):
        """Handle button clicks and execute the associated action."""
        if event == cv2.EVENT_LBUTTONDOWN:
            for button_id, (bounds, action) in self.buttons.items():
                x1, y1, x2, y2 = bounds
                if x1 <= x <= x2 and y1 <= y <= y2:
                    action()
                    break

    def clear_buttons(self):
        """Clear the stored buttons for the current frame."""
        self.buttons.clear()