# Serial_Shenanigans: COMedy Edition

<p align="center">
  <img src="icon.png" width="600" height="600">
</p>

Welcome to **Serial_Shenanigans: COMedy Edition** — a quirky, fun-filled project that brings serial communication to life with a comedic twist! This app lets you interact with your serial ports in a way you've never seen before, complete with playful sounds and humor.

If you've ever wanted to play around with serial communication and have a good laugh while you're at it, this is your ticket.

---

## 🚀 Features

- **COM Port Detection**: Automatically detect available serial ports on your machine.
- **Baudrate Selection**: Choose from a comprehensive list of standard baud rates.
- **Connect and Communicate**: Establish a connection to your serial port and start the fun.
- **Comedic Sounds**: Play system sounds and enjoy some lighthearted humor while you work.
- **Completely GUI-Driven**: No command line necessary. Just point, click, and laugh.
- **Real-Time Serial Communication**: View and send data seamlessly.

---

## 📁 Project Structure

The project directory includes:

- **Python Code**: The heart of the "Serial Shenanigans" experience.
- **Assets**: Images and icons for the GUI.
- **Installer**: A script to get everything set up quickly.
- **README.md**: The document you're reading right now.

---

## 📸 Screenshots

Here's a sneak peek at how the app looks:

<p align="center">
  <img src="screenshot.png">
</p>

---

## 💻 Getting Started

### Prerequisites

Before running the project, you'll need:

- Python 3.x
- `ttkbootstrap` library (for the fancy GUI)
- `pyserial` library (for serial communication)

### Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/your-username/Serial_Shenanigans-COMedy_Edition.git
   cd Serial_Shenanigans-COMedy_Edition
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. After installation, you're ready to start the app!

### Running the App

To launch the app:

```bash
python serial_app.py
```

A window will appear where you can:

- Select a COM port
- Choose a baud rate
- Hit **Connect** and start the shenanigans!

---

## 🎮 Code Snippet

Here’s a glimpse into the inner workings of the app:

```python
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import serial
import serial.tools.list_ports
import threading
import winsound

class SerialApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Serial Shenanigans: COMedy Edition")
        self.root.resizable(False, False)
        self.serial_port = None
        self.read_thread = None
        self.stop_thread = threading.Event()

        # Set window icon (optional)
        icon_image = ttk.PhotoImage(file="icon.png")
        root.tk.call("wm", "iconphoto", root._w, icon_image)

        # Frame for Port and Baudrate Configuration
        config_frame = ttk.Labelframe(root, text="Configuration", padding=10)
        config_frame.pack(fill=X, padx=10, pady=10)

        # COM Port Selection
        ttk.Label(config_frame, text="COM Port:").grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.port_var = ttk.StringVar()
        self.port_menu = ttk.Combobox(config_frame, textvariable=self.port_var, state="readonly")
        self.port_menu.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        self.refresh_ports()
```

---

## 💡 Contributing

I love contributions that add more fun, humor, and creativity to the project. Feel free to fork this repository, make your changes, and submit a pull request. Whether it's new features, more sounds, or funnier text, we welcome all ideas.

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE-MIT.txt](LICENSE-MIT.txt) file for details.

---

Now you're ready to have some fun with serial communication. Happy coding, and may your ports always stay open! 😎

---
