import tkinter as tk
from PIL import Image, ImageTk
import random
import ctypes
import os
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class DesktopPet:
    def __init__(self, master, gif_right_path, gif_left_path, start_pos=(100, 300)):
        self.master = master
        self.master.overrideredirect(True)
        self.master.wm_attributes("-topmost", True)
        self.master.wm_attributes("-transparentcolor", "white")

        user32 = ctypes.windll.user32
        self.virtual_origin_x = user32.GetSystemMetrics(76)
        self.virtual_origin_y = user32.GetSystemMetrics(77)
        self.virtual_width = user32.GetSystemMetrics(78)
        self.virtual_height = user32.GetSystemMetrics(79)

        self.frames_right = self.load_gif_frames(resource_path(gif_right_path))
        self.frames_left = self.load_gif_frames(resource_path(gif_left_path))
        self.current_frames = self.frames_right

        self.label = tk.Label(master, bg="white")
        self.label.pack()

        self.idx = 0
        self.direction = 1
        self.is_dragging = False
        self.pos_x, self.pos_y = start_pos

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

    def load_gif_frames(self, path):
        img = Image.open(path)
        frames = []
        try:
            while True:
                img.seek(len(frames))
                frames.append(ImageTk.PhotoImage(img.copy()))
        except EOFError:
            pass
        return frames

    def animate(self):
        frame = self.current_frames[self.idx]
        self.label.config(image=frame)
        self.idx = (self.idx + 1) % len(self.current_frames)
        self.master.after(100, self.animate)

    def start_drag(self, event):
        self.is_dragging = True
        self.offset_x = event.x
        self.offset_y = event.y

    def on_drag(self, event):
        new_x = event.x_root - self.offset_x
        new_y = event.y_root - self.offset_y

        if new_x > self.pos_x:
            self.direction = 1
            self.current_frames = self.frames_right
        elif new_x < self.pos_x:
            self.direction = -1
            self.current_frames = self.frames_left

        self.pos_x, self.pos_y = new_x, new_y
        self.master.geometry(f"+{self.pos_x}+{self.pos_y}")

    def stop_drag(self, event):
        self.is_dragging = False

    def auto_move(self):
        if not self.is_dragging:
            if random.random() < 0.2:
                self.set_idle()
            else:
                step_x = 15
                step_y = random.choice([-3, 0, 3])

                self.direction = random.choice([-1, 1])
                self.current_frames = (
                    self.frames_right if self.direction == 1 else self.frames_left
                )
                self.set_walk()

                self.pos_x += step_x * self.direction
                self.pos_y += step_y

                min_x = self.virtual_origin_x
                max_x = self.virtual_origin_x + self.virtual_width - 100
                self.pos_x = max(min_x, min(self.pos_x, max_x))

                min_y = self.virtual_origin_y
                max_y = self.virtual_origin_y + self.virtual_height - 100
                self.pos_y = max(min_y, min(self.pos_y, max_y))

                self.master.geometry(f"+{self.pos_x}+{self.pos_y}")

        self.master.after(1000, self.auto_move)

    def set_idle(self):
        self.current_frames = (
            self.frames_right if self.direction == 1 else self.frames_left
        )
        self.idx = 0

    def set_walk(self):
        self.current_frames = (
            self.frames_right if self.direction == 1 else self.frames_left
        )
        self.idx = 0

    def move_to(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.master.geometry(f"+{x}+{y}")

    # ✅ 右鍵選單顯示
    def show_menu(self, event):
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()
