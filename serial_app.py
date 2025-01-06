import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import serial
import serial.tools.list_ports
import threading
import winsound

class SerialApp:
    def __init__(self, root):
        """Initialize the SerialApp GUI and its components."""
        self.root = root
        self.root.title("Serial Shenanigans: COMedy Edition")
        self.root.resizable(False, False)
        self.serial_port = None  # Serial port object
        self.read_thread = None  # Thread for reading serial data
        self.stop_thread = threading.Event()  # Event to stop threads

        # Set window icon (optional)
        icon_image = ttk.PhotoImage(file="icon.png")
        root.tk.call("wm", "iconphoto", root._w, icon_image)

        # Define the sound enabled variable
        self.sound_enabled = ttk.BooleanVar(value=True)  # Default sound state is enabled

        # Frame for Port and Baudrate Configuration
        config_frame = ttk.Labelframe(root, text="Configuration", padding=10)
        config_frame.pack(fill=X, padx=10, pady=10)

        # COM Port Selection
        ttk.Label(config_frame, text="COM Port:").grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.port_var = ttk.StringVar()
        self.port_menu = ttk.Combobox(config_frame, textvariable=self.port_var, state="readonly")
        self.port_menu.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        self.refresh_ports()

        # Refresh Ports Button
        refresh_button = ttk.Button(config_frame, text="Refresh", bootstyle="info", command=self.refresh_ports)
        refresh_button.grid(row=0, column=2, padx=5, pady=5)

        # Baudrate Selection
        ttk.Label(config_frame, text="Baudrate:").grid(row=1, column=0, padx=5, pady=5)
        self.baud_var = ttk.StringVar(value="9600")
        baud_menu = ttk.Combobox(config_frame, textvariable=self.baud_var, state="readonly")
        # Include all standard baud rates
        baud_menu['values'] = ["110", "300", "1200", "2400", "4800", "9600", "14400", "19200", "38400", "57600", "115200", "230400", "460800", "921600"]
        baud_menu.grid(row=1, column=1, padx=5, pady=5)

        # Connect Button
        self.connect_button = ttk.Button(config_frame, text="Connect", bootstyle="success", command=self.connect_serial)
        self.connect_button.grid(row=2, column=0, columnspan=3, pady=10)

        # Frame for Sending and Receiving Data
        io_frame = ttk.Labelframe(root, text="Serial Communication", padding=10)
        io_frame.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        # Received Data Display
        ttk.Label(io_frame, text="Received:").grid(row=0, column=0, padx=5, pady=5)
        self.receive_text = ttk.Text(io_frame, height=10, width=50, state=NORMAL)
        self.receive_text.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        self.receive_text.config(state=DISABLED)

        # Clear Button
        clear_button = ttk.Button(io_frame, text="Clear", bootstyle="warning", command=self.clear_terminal)
        clear_button.grid(row=2, column=0, padx=5, pady=5)

        # Message to Send
        ttk.Label(io_frame, text="Message:").grid(row=3, column=0, padx=5, pady=5)
        self.send_var = ttk.StringVar()
        send_entry = ttk.Entry(io_frame, textvariable=self.send_var, width=40)
        send_entry.grid(row=3, column=1, padx=5, pady=5)

        # End-of-Line Selection
        ttk.Label(io_frame, text="EOL:").grid(row=4, column=0, padx=5, pady=5)
        self.eol_var = ttk.StringVar(value="<lf>")
        eol_menu = ttk.Combobox(io_frame, textvariable=self.eol_var, state="readonly")
        eol_menu['values'] = ["<cr>", "<lf>", "<cr><lf>", "<none>"]
        eol_menu.grid(row=4, column=1, padx=5, pady=5)

        # Send Button
        send_button = ttk.Button(io_frame, text="Send", bootstyle="primary", command=self.send_message)
        send_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Author and GitHub Link
        self.author_label = ttk.Label(root, text="Created by Alireza Jahanbakhshi", bootstyle="info", cursor="hand2")
        self.author_label.pack(pady=10)
        self.author_label.bind("<Button-1>", self.open_github)

        # Sound Toggle Checkbox
        sound_toggle = ttk.Checkbutton(
            config_frame,
            text="Enable Sounds",
            variable=self.sound_enabled,
            command=self.toggle_sound,
            bootstyle="round-toggle-success",
        )
        sound_toggle.grid(row=3, column=0, columnspan=3, pady=5)

    def open_github(self, event):
        """Open GitHub profile when the label is clicked."""
        import webbrowser
        webbrowser.open("https://github.com/Alireza-Jahanbakhshi")

    def play_sound(self, file_path=None):
        """Play or stop a sound based on the toggle state."""
        if self.sound_enabled.get():  # Check if sound is enabled
            if file_path:
                winsound.PlaySound(file_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
            else:
                # Optionally play a default beep if no file is provided
                winsound.Beep(1000, 500)
        else:
            # Stop any currently playing sounds
            winsound.PlaySound(None, winsound.SND_ASYNC)

    def toggle_sound(self):
        """Toggle sound on or off."""
        if not self.sound_enabled.get():  # If the toggle is turned off
            self.play_sound()  # This will stop any sounds playing

    def refresh_ports(self):
        """Refresh the list of available COM ports."""
        ports = serial.tools.list_ports.comports()
        self.port_menu['values'] = [port.device for port in ports]
        if ports:
            self.port_var.set(ports[0].device)  # Automatically select the first port

    def connect_serial(self):
        """Connect or disconnect the serial port."""
        if self.serial_port and self.serial_port.is_open:
            # Disconnect the serial port
            self.stop_thread.set()
            if self.read_thread:
                self.read_thread.join()
            self.serial_port.close()
            self.serial_port = None
            self.connect_button.config(text="Connect", bootstyle="success")
            self.root.update_idletasks()  # Ensure GUI updates before playing the sound
            self.play_sound("disconnect_sound.wav")  # Play disconnection sound
        else:
            try:
                # Connect to the serial port
                self.serial_port = serial.Serial(
                    port=self.port_var.get(),
                    baudrate=int(self.baud_var.get()),
                    timeout=0.01  # Non-blocking read
                )
                self.stop_thread.clear()
                self.read_thread = threading.Thread(target=self.read_from_serial_thread, daemon=True)
                self.read_thread.start()
                self.connect_button.config(text="Disconnect", bootstyle="danger")
                self.root.update_idletasks()  # Ensure GUI updates before playing the sound
                self.play_sound("connect_sound.wav")  # Play connection sound
            except serial.SerialException as e:
                ttk.Messagebox.show_error("Error", str(e))

    def read_from_serial_thread(self):
        """Read data from the serial port in a separate thread."""
        buffer = ""
        while not self.stop_thread.is_set():
            if self.serial_port and self.serial_port.is_open:
                try:
                    data = self.serial_port.read(1024)  # Read up to 1024 bytes
                    if data:
                        buffer += data.decode('utf-8', errors='ignore')
                        if "\n" in buffer:  # Process complete lines
                            lines = buffer.split("\n")
                            for line in lines[:-1]:
                                self.root.after(0, self.update_receive_text, line + "\n")
                            buffer = lines[-1]  # Save remaining data
                except Exception as e:
                    print(f"Error reading from serial port: {e}")

    def update_receive_text(self, data):
        """Update the received text area in the GUI thread."""
        self.receive_text.config(state=NORMAL)
        self.receive_text.insert(END, data)
        self.receive_text.see(END)  # Auto-scroll to the end
        self.receive_text.config(state=DISABLED)

    def send_message(self):
        """Send a message to the serial port."""
        if self.serial_port and self.serial_port.is_open:
            message = self.send_var.get()
            if message:
                # Append selected EOL character(s)
                eol = self.eol_var.get()
                if eol == "<cr>":
                    message += "\r"
                elif eol == "<lf>":
                    message += "\n"
                elif eol == "<cr><lf>":
                    message += "\r\n"
                # Send the message
                self.serial_port.write(message.encode('utf-8'))
        else:
            ttk.Messagebox.show_error("Error", "Serial port is not connected.")

    def clear_terminal(self):
        """Clear the received text display."""
        self.receive_text.config(state=NORMAL)
        self.receive_text.delete(1.0, END)
        self.receive_text.config(state=DISABLED)

if __name__ == "__main__":
    root = ttk.Window(themename="vapor")
    root.resizable(False, False)
    app = SerialApp(root)
    root.mainloop()
