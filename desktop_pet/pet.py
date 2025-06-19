import tkinter as tk
import random
import ctypes
import sys
from enum import Enum, auto

from .utils import resource_path, load_gif_frames


class PetState(Enum):
    IDLE = auto()
    WALK = auto()
    DRAG = auto()
    DASH = auto()


class DesktopPet:
    def __init__(
        self,
        master,
        gif_right_path,
        gif_left_path,
        start_pos=(100, 300),
        max_dash_distance=200,
    ):
        self.master = master
        self.master.overrideredirect(True)
        self.master.wm_attributes("-topmost", True)
        try:
            # Windows supports transparentcolor and multi-monitor metrics
            self.master.wm_attributes("-transparentcolor", "white")
        except tk.TclError:
            # Other platforms use a different attribute name for transparency
            self.master.attributes("-transparent", "white")

        if sys.platform.startswith("win"):
            user32 = ctypes.windll.user32
            self.virtual_origin_x = user32.GetSystemMetrics(76)
            self.virtual_origin_y = user32.GetSystemMetrics(77)
            self.virtual_width = user32.GetSystemMetrics(78)
            self.virtual_height = user32.GetSystemMetrics(79)
        else:
            # Fall back to the main screen size on non-Windows systems
            self.virtual_origin_x = 0
            self.virtual_origin_y = 0
            self.virtual_width = self.master.winfo_screenwidth()
            self.virtual_height = self.master.winfo_screenheight()

        self.frames_right = load_gif_frames(resource_path(gif_right_path))
        self.frames_left = load_gif_frames(resource_path(gif_left_path))
        self.current_frames = self.frames_right

        self.label = tk.Label(master, bg="white")
        self.label.pack()

        self.idx = 0
        self.direction = 1
        self.walk_steps_remaining = 0
        self.state = PetState.IDLE
        self.pos_x, self.pos_y = start_pos

        # Dash related
        self.dash_remaining = 0
        self.dash_step_x = 0
        self.dash_step_y = 0
        self.max_dash_distance = max_dash_distance

        # 拖曳
        self.label.bind("<Button-1>", self.start_drag)
        self.label.bind("<B1-Motion>", self.on_drag)
        self.label.bind("<ButtonRelease-1>", self.stop_drag)

        # ✅ 加入右鍵選單
        self.label.bind("<Button-3>", self.show_menu)

        self.menu = tk.Menu(master, tearoff=0)
        self.menu.add_command(label="退出", command=master.destroy)

        self.animate()
        self.auto_move()
        self.master.geometry(f"+{self.pos_x}+{self.pos_y}")

    def animate(self):
        frame = self.current_frames[self.idx]
        self.label.config(image=frame)
        self.idx = (self.idx + 1) % len(self.current_frames)
        self.master.after(100, self.animate)

    def start_drag(self, event):
        self.state = PetState.DRAG
        self.offset_x = event.x
        self.offset_y = event.y

    def on_drag(self, event):
        if self.state != PetState.DRAG:
            return

        new_x = event.x_root - self.offset_x

        if new_x > self.pos_x:
            self.direction = 1
            self.current_frames = self.frames_right
        elif new_x < self.pos_x:
            self.direction = -1
            self.current_frames = self.frames_left

        self.pos_x = new_x
        self.master.geometry(f"+{self.pos_x}+{self.pos_y}")

    def stop_drag(self, event):
        self.state = PetState.IDLE

    def auto_move(self):
        if self.state not in (PetState.DRAG, PetState.DASH):
            if random.random() < 0.01:
                self.start_dash()
            elif random.random() < 0.1:
                self.set_idle()
            else:
                step_x = 8

                if self.walk_steps_remaining <= 0:
                    self.direction = random.choice([-1, 1])
                    self.walk_steps_remaining = random.randint(3, 7)
                self.current_frames = (
                    self.frames_right if self.direction == 1 else self.frames_left
                )
                self.set_walk()
                self.walk_steps_remaining -= 1

                self.pos_x += step_x * self.direction

                min_x = self.virtual_origin_x
                max_x = self.virtual_origin_x + self.virtual_width - 100
                self.pos_x = max(min_x, min(self.pos_x, max_x))


                self.master.geometry(f"+{int(self.pos_x)}+{int(self.pos_y)}")

        self.master.after(1000, self.auto_move)

    def set_idle(self):
        self.current_frames = (
            self.frames_right if self.direction == 1 else self.frames_left
        )
        self.idx = 0
        self.state = PetState.IDLE

    def set_walk(self):
        self.current_frames = (
            self.frames_right if self.direction == 1 else self.frames_left
        )
        self.idx = 0
        self.state = PetState.WALK

    def start_dash(self):
        """Start a short dash toward the current mouse cursor position."""
        pointer_x = self.master.winfo_pointerx()
        pointer_y = self.pos_y

        dx = pointer_x - self.pos_x
        dy = 0
        distance = abs(dx)

        if distance > self.max_dash_distance:
            scale = self.max_dash_distance / distance
            pointer_x = self.pos_x + dx * scale
            dx = pointer_x - self.pos_x
            dy = 0

        steps = 10
        self.dash_step_x = dx / steps
        self.dash_step_y = 0
        self.dash_remaining = steps

        self.direction = 1 if self.dash_step_x >= 0 else -1
        self.current_frames = (
            self.frames_right if self.direction == 1 else self.frames_left
        )
        self.state = PetState.DASH
        self.dash_move()

    def dash_move(self):
        if self.dash_remaining <= 0 or self.state != PetState.DASH:
            self.state = PetState.IDLE
            return

        self.pos_x += self.dash_step_x

        min_x = self.virtual_origin_x
        max_x = self.virtual_origin_x + self.virtual_width - 100
        self.pos_x = max(min_x, min(self.pos_x, max_x))


        self.master.geometry(f"+{int(self.pos_x)}+{int(self.pos_y)}")

        self.dash_remaining -= 1
        self.master.after(50, self.dash_move)

    def move_to(self, x, y=None):
        self.pos_x = x
        self.master.geometry(f"+{int(x)}+{int(self.pos_y)}")

    # ✅ 右鍵選單顯示
    def show_menu(self, event):
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()
