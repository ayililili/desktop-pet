import tkinter as tk
from desktop_pet.pet import DesktopPet

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # 暫時隱藏主視窗，避免在計算螢幕寬高時出現閃爍

    # 取得主螢幕尺寸
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 寵物寬高大約 100x100（你可以依實際 gif 調整）
    pet_width = 100
    pet_height = 100

    # 計算置中位置
    start_x = (screen_width - pet_width) // 2
    start_y = (screen_height - pet_height) // 2

    root.deiconify()  # 顯示主視窗
    pet = DesktopPet(
        master=root,
        gif_right_path="assets/pet_right.gif",
        gif_left_path="assets/pet_left.gif",
        start_pos=(start_x, start_y),
    )
    root.mainloop()
