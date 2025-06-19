import tkinter as tk
from desktop_pet.pet import DesktopPet

if __name__ == "__main__":
    root = tk.Tk()
    start_x = 100
    start_y = 300
    pet = DesktopPet(
        master=root,
        gif_right_path="assets/pet_right.gif",
        gif_left_path="assets/pet_left.gif",
        start_pos=(start_x, start_y),
    )
    root.mainloop()
