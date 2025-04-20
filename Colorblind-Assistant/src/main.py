import sys
import threading
import logging
from dataclasses import dataclass
from typing import Tuple, Optional
import colorsys
import customtkinter as ctk
from pynput import keyboard, mouse
from mss import mss
from PIL import Image
from colors import COLORS

# Application configuration constants
APP_CONFIG = {
    "FPS": 60,
    "THEME_MODE": "dark",
    "THEME_COLOR": "blue",
    "HOTKEY_TOGGLE": {keyboard.Key.alt, keyboard.Key.alt_l, keyboard.Key.alt_r},
    "HOTKEY_EXIT": keyboard.Key.f1,
    "UI": {
        "OFFSET_X": 16,
        "OFFSET_Y": 16,
        "TOOLTIP_CORNER_RADIUS": 8,
        "TOOLTIP_FG_COLOR": "#2b2b2b",
        "PREVIEW_SIZE": 32,
        "PREVIEW_CORNER_RADIUS": 4,
        "PREVIEW_DEFAULT_COLOR": "#555555",
        "FONT_HEADER": ("Tahoma", 13, "bold"),
        "FONT_BODY": ("Tahoma", 11),
        "GRAB_INTERVAL_MS": 1000 // 60,  # Recalculated based on FPS
    },
}

APP_CONFIG["UI"]["GRAB_INTERVAL_MS"] = (
    1000 // APP_CONFIG["FPS"]
)  # Real-time frame rate calculation

# Configure logging for tracking errors and performance
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


@dataclass(frozen=True)
class ColorInfo:
    """Data structure for holding color information."""

    name: str
    category: str
    rgb: Tuple[int, int, int]
    hex_code: str


class ColorUtils:
    """Utility class for color conversions and matching."""

    @staticmethod
    def rgb_to_hsv(rgb: Tuple[int, int, int]) -> Tuple[float, float, float]:
        """Converts RGB color values to HSV."""
        r, g, b = (channel / 255 for channel in rgb)
        return colorsys.rgb_to_hsv(r, g, b)

    @staticmethod
    def hsv_distance(
        hsv1: Tuple[float, float, float], hsv2: Tuple[float, float, float]
    ) -> float:
        """
        Calculates perceptual distance between two HSV colors.
        This is useful for finding the closest color in a predefined set.
        """
        h1, s1, v1 = hsv1
        h2, s2, v2 = hsv2
        dh = min(abs(h1 - h2), 1 - abs(h1 - h2)) * 2  # Weighted hue component
        ds = abs(s1 - s2)
        dv = abs(v1 - v2)
        return dh + ds + dv

    @staticmethod
    def find_nearest_color(rgb: Tuple[int, int, int]) -> Optional[ColorInfo]:
        """
        Finds the closest named color from a predefined list based on HSV distance.
        This method compares the input RGB color to a set of predefined colors and returns
        the nearest match.
        """
        target_hsv = ColorUtils.rgb_to_hsv(rgb)
        min_distance = float("inf")
        nearest = None

        # Iterate over predefined colors
        for name, (color_rgb, category) in COLORS.items():
            current_hsv = ColorUtils.rgb_to_hsv(color_rgb)
            distance = ColorUtils.hsv_distance(target_hsv, current_hsv)

            if distance < min_distance:
                min_distance = distance
                nearest = (name, category, color_rgb)

        if not nearest:
            return None

        # Return the color information as a ColorInfo object
        name, category, _ = nearest
        return ColorInfo(
            name=name,
            category=category,
            rgb=rgb,
            hex_code=f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}",
        )


class ColorTooltip(ctk.CTkToplevel):
    """A custom tooltip for displaying color details."""

    def __init__(self, master: ctk.CTk):
        """Initialize the tooltip window and its components."""
        super().__init__(master)
        self._initialize_window()
        self._create_widgets()
        self._visible = False

    def _initialize_window(self) -> None:
        """Initialize window properties like topmost and no border."""
        self.withdraw()  # Initially hide the window
        self.overrideredirect(True)  # Remove window borders
        self.attributes("-topmost", True)  # Keep the window on top

    def _create_widgets(self) -> None:
        """
        Create and arrange UI elements for displaying color info.
        This includes labels for the color name, category, RGB, HEX,
        and a color preview.
        """
        self.frame = ctk.CTkFrame(
            self,
            corner_radius=APP_CONFIG["UI"]["TOOLTIP_CORNER_RADIUS"],
            fg_color=APP_CONFIG["UI"]["TOOLTIP_FG_COLOR"],
        )
        self.frame.pack(padx=8, pady=8)

        # Add labels and preview
        self.label_name = ctk.CTkLabel(
            self.frame, text="", font=APP_CONFIG["UI"]["FONT_HEADER"]
        )
        self.label_category = ctk.CTkLabel(
            self.frame, text="", font=APP_CONFIG["UI"]["FONT_BODY"]
        )
        self.label_rgb = ctk.CTkLabel(
            self.frame, text="", font=APP_CONFIG["UI"]["FONT_BODY"]
        )
        self.label_hex = ctk.CTkLabel(
            self.frame, text="", font=APP_CONFIG["UI"]["FONT_BODY"]
        )
        self.preview_frame = ctk.CTkFrame(
            self.frame,
            width=APP_CONFIG["UI"]["PREVIEW_SIZE"],
            height=APP_CONFIG["UI"]["PREVIEW_SIZE"],
            corner_radius=APP_CONFIG["UI"]["PREVIEW_CORNER_RADIUS"],
            fg_color=APP_CONFIG["UI"]["PREVIEW_DEFAULT_COLOR"],
        )

        # Arrange UI components
        self.preview_frame.grid(row=0, column=1, rowspan=4, padx=(0, 12), pady=4)
        self.label_name.grid(row=0, column=0, sticky="w")
        self.label_category.grid(row=1, column=0, sticky="w")
        self.label_rgb.grid(row=2, column=0, sticky="w")
        self.label_hex.grid(row=3, column=0, sticky="w")

    def update_info(self, info: ColorInfo, x: int, y: int) -> None:
        """
        Update the tooltip with the latest color information.
        The tooltip is displayed at the given (x, y) screen coordinates.
        """
        self.label_name.configure(text=info.name.upper())
        self.label_category.configure(text=f"Category: {info.category}")
        self.label_rgb.configure(text=f"RGB: {info.rgb}")
        self.label_hex.configure(text=f"HEX: {info.hex_code}")
        self.preview_frame.configure(fg_color=info.hex_code)
        self.geometry(
            f"+{x + APP_CONFIG['UI']['OFFSET_X']}+{y + APP_CONFIG['UI']['OFFSET_Y']}"
        )

    def show(self) -> None:
        """Display the tooltip."""
        if not self._visible:
            self.deiconify()
            self._visible = True

    def hide(self) -> None:
        """Hide the tooltip."""
        if self._visible:
            self.withdraw()
            self._visible = False


class ColorSampler:
    """Handles the process of sampling colors based on mouse position and hotkeys."""

    def __init__(self, tooltip: ColorTooltip):
        """Initialize the color sampler with a tooltip for displaying results."""
        self.tooltip = tooltip
        self.mouse_controller = mouse.Controller()
        self.sampling_active = threading.Event()
        self.keyboard_listener = None

    def start(self) -> None:
        """Start continuous color sampling."""
        if not self.sampling_active.is_set():
            logging.info("Color sampling started")
            self.sampling_active.set()
            self.tooltip.show()
            self._sampling_loop()

    def stop(self) -> None:
        """Stop continuous color sampling."""
        if self.sampling_active.is_set():
            logging.info("Color sampling stopped")
            self.sampling_active.clear()
            self.tooltip.hide()

    def _sampling_loop(self) -> None:
        """
        Main loop that continually samples the color under the cursor.
        This method grabs the pixel color and updates the tooltip.
        """
        if not self.sampling_active.is_set():
            return

        try:
            x, y = self.mouse_controller.position
            with mss() as sct:
                img = sct.grab({"left": x, "top": y, "width": 1, "height": 1})

            r, g, b = img.pixel(0, 0)
            color_info = ColorUtils.find_nearest_color((r, g, b))

            if color_info:
                self.tooltip.update_info(color_info, x, y)

        except Exception as e:
            logging.error(f"Sampling error: {str(e)}")
        finally:
            self.tooltip.after(
                APP_CONFIG["UI"]["GRAB_INTERVAL_MS"], self._sampling_loop
            )

    def bind_hotkeys(self) -> None:
        """
        Bind the hotkeys for starting and stopping color sampling.
        The hotkey to toggle sampling is configured in the APP_CONFIG.
        """

        def on_press(key):
            if key in APP_CONFIG["HOTKEY_TOGGLE"]:
                self.start()
            elif key == APP_CONFIG["HOTKEY_EXIT"]:
                logging.info("Exit command received")
                sys.exit(0)

        def on_release(key):
            if key in APP_CONFIG["HOTKEY_TOGGLE"]:
                self.stop()

        self.keyboard_listener = keyboard.Listener(
            on_press=on_press, on_release=on_release, daemon=True
        )
        self.keyboard_listener.start()


def main() -> None:
    """Main function to run the application."""
    try:
        # Set up the application appearance mode and theme color
        ctk.set_appearance_mode(APP_CONFIG["THEME_MODE"])
        ctk.set_default_color_theme(APP_CONFIG["THEME_COLOR"])

        # Initialize the main window and tooltip
        root = ctk.CTk()
        root.withdraw()

        tooltip = ColorTooltip(root)
        sampler = ColorSampler(tooltip)
        sampler.bind_hotkeys()

        root.mainloop()

    except Exception as e:
        logging.critical(f"Critical error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
