import os
import sys
from PIL import Image, ImageTk


def resource_path(relative_path: str) -> str:
    """Resolve resource path for PyInstaller or normal execution."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def load_gif_frames(path: str):
    """Load all frames from a GIF and return as a list of PhotoImage."""
    img = Image.open(path)
    frames = []
    try:
        while True:
            img.seek(len(frames))
            frames.append(ImageTk.PhotoImage(img.copy()))
    except EOFError:
        pass
    return frames
