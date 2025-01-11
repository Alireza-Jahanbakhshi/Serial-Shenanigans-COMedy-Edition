# Serial_Shenanigans: COMedy Edition

<p align="center">
  <img src="icon.png" width="600" height="600">
</p>

Welcome to **Serial_Shenanigans: COMedy Edition** — a quirky, fun-filled project that brings serial communication to life with a comedic twist! This app lets you interact with your serial ports in a way you've never seen before, complete with playful sounds and humor.

If you've ever wanted to play around with serial communication and have a good laugh while you're at it, this is your ticket.

---

## 🚀 Features

### 1. Serial Port Configuration
- **Dynamic COM Port Detection**: Automatically detects and lists available serial ports on your system.
- **Refresh Option**: Updates the COM port list in real-time.
- **Customizable Baud Rate Settings**: Select from a comprehensive list of standard baud rates.

### 2. Connection Management
- **Connect/Disconnect Functionality**: Seamlessly establish or terminate connections to the selected COM port.
- **Advanced Serial Settings**:
  - **Parity Configuration**: Supports None, Odd, Even, Mark, and Space.
  - **Adjustable Data Bits**: Choose from 5, 6, 7, or 8 data bits.
  - **Flexible Stop Bits Options**: Configure to 1, 1.5, or 2 stop bits.
  - **Flow Control Mechanisms**: Supports None, XON/XOFF, RTS/CTS, and DSR/DTR.

### 3. Data Management and Processing
- **Real-Time Data Monitoring**: View incoming data in a dedicated text area.
- **Timestamp Integration**: Toggle timestamps to include date and time with each received message.
- **Data Export Options**:
  - Export received data to `.txt`, `.csv`, or `.json` formats.
- **Clear Display**: Instantly clear the data display area with a single click.

### 4. Message Transmission
- **Custom Message Input**: Enter and send user-defined messages.
- **End-of-Line Character Options**:
  - Predefined choices: `<cr>`, `<lf>`, `<cr><lf>`, and `<none>`.
  - **Custom EOL Definition**: Option to define and use custom EOL characters.

### 5. User Experience Enhancements
- **Sound Feedback**:
  - Notification sounds for connection, disconnection, and other key actions.
  - Easily toggle sound effects on or off.
- **Modern GUI Design**:
  - Built with ttkbootstrap for a professional and responsive user interface.
  - Compact layout with enhanced usability.
  - Scrollable text area for managing extensive data streams.

### 6. Error Handling and Notifications
- **Connection Error Messages**: Provides clear feedback for issues like unavailable ports or connection failures.
- **Export Failures**: Alerts the user if data export encounters errors.

### 7. Developer-Friendly Features
- **Author Attribution and GitHub Integration**:
  - Quick access to the author’s GitHub profile for further collaboration.

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

Before running the project, ensure you have the following installed:

1. **Python**: Version 3.x is required.
2. **Dependencies**:
   - `ttkbootstrap`: For enhanced GUI components and themes.
   - `pyserial`: To enable serial communication with COM ports.
   - `winsound` *(Windows-only)*: For sound notifications.
   - `json` *(built-in)*: For handling data serialization.
   - `datetime` *(built-in)*: For generating timestamps.

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
