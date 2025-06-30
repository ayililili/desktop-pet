# Desktop Pet

A simple desktop pet implemented in Python with `tkinter`. The pet walks around the screen and can be dragged with the mouse. When your cursor comes within 300 pixels of the pet it performs a short dash horizontally toward the cursor's vertical position. When walking normally, the pet now chooses a direction and continues for a few steps before deciding where to go next. The code detects the operating system and works on Windows, macOS and Linux.

## Requirements

- Python 3
- Pillow

Install Pillow with:

```bash
pip install pillow
```

## Usage

Run the main script on any platform that supports `tkinter`:

```bash
python main.py
```

The application will create a frameless window with an animated GIF of the pet.

## Release

To build a standalone executable, install PyInstaller:

```bash
pip install pyinstaller
```

Generate the executable from `main.py`:

```bash
pyinstaller --onefile --add-data "assets{}assets" main.py
```

Replace `{}` with `;` on Windows or `:` on Linux/macOS. PyInstaller places the output under the `dist/` directory. Ensure the `assets/` folder sits alongside the executable if you do not embed it.
