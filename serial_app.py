import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox  
import serial
import serial.tools.list_ports
import threading
import winsound  
import json
from tkinter import filedialog
from datetime import datetime

class SerialApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Serial Shenanigans: COMedy Edition")
        self.root.resizable(False, False)
        self.serial_port = None # Serial port object
        self.read_thread = None # Thread for reading serial data
        self.stop_thread = threading.Event() # Event to stop threads

        # Set window icon (optional)
        icon_image = ttk.PhotoImage(file="icon.png")
        root.tk.call("wm", "iconphoto", root._w, icon_image)

        # Define the sound enabled variable
        self.sound_enabled = ttk.BooleanVar(value=True)  # Default sound state as enabled

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
        self.baud_var = ttk.StringVar(value="115200")
        baud_menu = ttk.Combobox(config_frame, textvariable=self.baud_var, state="readonly")
        baud_menu['values'] = ["110", "300", "1200", "2400", "4800", "9600", "14400", "19200", "38400", "57600", "115200", "230400", "460800", "921600"]
        baud_menu.grid(row=1, column=1, padx=5, pady=5)

        # Connect Button
        self.connect_button = ttk.Button(config_frame, text="Connect", bootstyle="success", command=self.connect_serial)
        self.connect_button.grid(row=2, column=0, columnspan=3, pady=10)

        # Frame for Sending and Receiving Data
        io_frame = ttk.Labelframe(root, text="Serial Communication", padding=10)
        io_frame.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        # Received Data Display with Scrollbar
        ttk.Label(io_frame, text="Received:").grid(row=0, column=0, padx=5, pady=5)
        self.receive_text = ttk.Text(io_frame, height=10, width=50, wrap='word', state=DISABLED)
        self.receive_text.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='nsew')

        # Add Scrollbar
        scrollbar = ttk.Scrollbar(io_frame, orient='vertical', command=self.receive_text.yview)
        scrollbar.grid(row=1, column=2, sticky='ns')
        self.receive_text.config(yscrollcommand=scrollbar.set)

        # Row for Clear, Export, and Timestamp Toggle
        button_frame = ttk.Frame(io_frame)  # Create a sub-frame to align buttons
        button_frame.grid(row=2, column=0, columnspan=3, pady=5, sticky='w')

        # Clear Button
        clear_button = ttk.Button(button_frame, text="Clear", bootstyle="warning", command=self.clear_terminal)
        clear_button.grid(row=0, column=0, padx=5, pady=5)

        # Export Button
        export_button = ttk.Button(button_frame, text="Export Data", bootstyle="info", command=self.export_data)
        export_button.grid(row=0, column=1, padx=5, pady=5)

        # Timestamp Toggle
        self.save_timestamp = ttk.BooleanVar(value=True)  # Default: Include timestamps
        timestamp_toggle = ttk.Checkbutton(
            button_frame,
            text="Include Timestamps",
            variable=self.save_timestamp,
            bootstyle="round-toggle-success",
        )
        timestamp_toggle.grid(row=0, column=2, padx=5, pady=5)

        # Message to Send
        ttk.Label(io_frame, text="Message:").grid(row=3, column=0, padx=5, pady=5)
        self.send_var = ttk.StringVar()
        send_entry = ttk.Entry(io_frame, textvariable=self.send_var, width=40)
        send_entry.grid(row=3, column=1, padx=5, pady=5)

        # End-of-Line Selection
        ttk.Label(io_frame, text="EOL:").grid(row=4, column=0, padx=5, pady=5, sticky='w')

        self.eol_var = ttk.StringVar(value="<lf>")
        eol_menu = ttk.Combobox(io_frame, textvariable=self.eol_var, state="readonly", width=12)
        eol_menu['values'] = ["<cr>", "<lf>", "<cr><lf>", "<none>", "Other"]
        eol_menu.grid(row=4, column=1, padx=5, pady=5, sticky='nwes')  # Slight right padding for spacing

        # Custom EOL Entry (initially hidden)
        self.custom_eol_var = ttk.StringVar()
        self.custom_eol_entry = ttk.Entry(io_frame, textvariable=self.custom_eol_var, width=12)
        self.custom_eol_entry.grid(row=5, column=1, padx=5, pady=5,sticky='nwes')  # Slight left padding for spacing
        self.custom_eol_entry.grid_remove()  # Hide by default

        # Bind event to show/hide custom EOL entry
        def toggle_custom_eol(*args):
            if self.eol_var.get() == "Other":
                self.custom_eol_entry.grid()  # Show entry
            else:
                self.custom_eol_entry.grid_remove()  # Hide entry

        self.eol_var.trace_add("write", toggle_custom_eol)

        # Send Button
        send_button = ttk.Button(io_frame, text="Send", bootstyle="primary", command=self.send_message)
        send_button.grid(row=6, column=0, columnspan=2, pady=10)

        # Author and GitHub Link
        self.author_label = ttk.Label(root, text="Created by Alireza Jahanbakhshi", bootstyle="info", cursor="hand2")
        self.author_label.pack(pady=10)
        self.author_label.bind("<Button-1>", self.open_github)

        # Sound Toggle Checkbox
        # Bind this new method to the checkbutton
        sound_toggle = ttk.Checkbutton(
            config_frame,
            text="Enable Sounds",
            variable=self.sound_enabled,
            command=self.toggle_sound,  # Add the toggle method
            bootstyle="round-toggle-success",
        )
        sound_toggle.grid(row=3, column=0, columnspan=3, pady=5)

        # Advanced Serial Settings
        ttk.Label(config_frame, text="Parity:").grid(row=4, column=0, padx=5, pady=5, sticky='nsew')
        self.parity_var = ttk.StringVar(value="None")
        parity_menu = ttk.Combobox(config_frame, textvariable=self.parity_var, state="readonly")
        parity_menu['values'] = ["None", "Odd", "Even", "Mark", "Space"]
        parity_menu.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(config_frame, text="Data Bits:").grid(row=5, column=0, padx=5, pady=5, sticky='nsew')
        self.data_bits_var = ttk.StringVar(value="8")
        data_bits_menu = ttk.Combobox(config_frame, textvariable=self.data_bits_var, state="readonly")
        data_bits_menu['values'] = ["5", "6", "7", "8"]
        data_bits_menu.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(config_frame, text="Stop Bits:").grid(row=6, column=0, padx=5, pady=5, sticky='nsew')
        self.stop_bits_var = ttk.StringVar(value="1")
        stop_bits_menu = ttk.Combobox(config_frame, textvariable=self.stop_bits_var, state="readonly")
        stop_bits_menu['values'] = ["1", "1.5", "2"]
        stop_bits_menu.grid(row=6, column=1, padx=5, pady=5)

        ttk.Label(config_frame, text="Flow Control:").grid(row=7, column=0, padx=5, pady=5, sticky='nsew')
        self.flow_control_var = ttk.StringVar(value="None")
        flow_control_menu = ttk.Combobox(config_frame, textvariable=self.flow_control_var, state="readonly")
        flow_control_menu['values'] = ["None", "XON/XOFF", "RTS/CTS", "DSR/DTR"]
        flow_control_menu.grid(row=7, column=1, padx=5, pady=5)

    def parse_line(self, line):
        """Parse a line of data into timestamp and message."""
        if "]" in line:  # Assume format like [timestamp] message
            parts = line.split("] ", 1)
            timestamp = parts[0].strip("[]")
            message = parts[1].strip()
            return timestamp, message
        else:
            return "", line.strip()  # No timestamp, return raw message

    def connect_serial(self):
        """Connect or disconnect the serial port."""
        if self.serial_port and self.serial_port.is_open:
            # Disconnect
            self.stop_thread.set()
            if self.read_thread:
                self.read_thread.join()
            self.serial_port.close()
            self.serial_port = None
            self.connect_button.config(text="Connect", bootstyle="success")
            self.root.update_idletasks()  # Ensure GUI updates before playing the sound
            self.play_sound("disconnect_sound.wav")  # Add sound for disconnection
        else:
            try:
                # Map parity settings
                parity_mapping = {
                    "None": serial.PARITY_NONE,
                    "Odd": serial.PARITY_ODD,
                    "Even": serial.PARITY_EVEN,
                    "Mark": serial.PARITY_MARK,
                    "Space": serial.PARITY_SPACE
                }
                # Map stop bits settings
                stop_bits_mapping = {
                    "1": serial.STOPBITS_ONE,
                    "1.5": serial.STOPBITS_ONE_POINT_FIVE,
                    "2": serial.STOPBITS_TWO
                }
                # Map flow control settings
                flow_control_mapping = {
                    "None": False,
                    "XON/XOFF": serial.XON_XOFF,
                    "RTS/CTS": serial.RTSCTS,
                    "DSR/DTR": serial.DSRDTR
                }

                # Connect
                self.serial_port = serial.Serial(
                    port=self.port_var.get(),
                    baudrate=int(self.baud_var.get()),
                    parity=parity_mapping[self.parity_var.get()],
                    stopbits=stop_bits_mapping[self.stop_bits_var.get()],
                    bytesize=int(self.data_bits_var.get()),
                    timeout=0.01,  # Non-blocking read
                    xonxoff=flow_control_mapping["XON/XOFF"],
                    rtscts=flow_control_mapping["RTS/CTS"],
                    dsrdtr=flow_control_mapping["DSR/DTR"]
                )
                self.stop_thread.clear()
                self.read_thread = threading.Thread(target=self.read_from_serial_thread, daemon=True)
                self.read_thread.start()
                self.connect_button.config(text="Disconnect", bootstyle="danger")
                self.root.update_idletasks()  # Ensure GUI updates before playing the sound
                self.play_sound("connect_sound.wav")  # Add sound for connection
            except serial.SerialException as e:
                ttk.Messagebox.show_error("Error", str(e))

    def open_github(self, event):
        """Open GitHub profile when clicked."""
        import webbrowser
        webbrowser.open("https://github.com/Alireza-Jahanbakhshi")

    def play_sound(self, file_path=None):
        """Play or stop a sound based on the toggle state."""
        if self.sound_enabled.get():  # Check if sound is enabled
            if file_path:
                winsound.PlaySound(file_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
            else:
                # Optionally play a default beep if no file is provided and sound is enabled
                winsound.Beep(1000, 500)
        else:
            # Stop any currently playing sounds if sound is disabled
            winsound.PlaySound(None, winsound.SND_ASYNC)

    def toggle_sound(self):
        """Toggle sound on or off."""
        if not self.sound_enabled.get():  # If the toggle is turned off
            self.play_sound()  # This will stop any sounds playing

    def refresh_ports(self):
        """Refresh available COM ports."""
        ports = serial.tools.list_ports.comports()
        self.port_menu['values'] = [port.device for port in ports]
        if ports:
            self.port_var.set(ports[0].device)

    def connect_serial(self):
        """Connect or disconnect the serial port."""
        if self.serial_port and self.serial_port.is_open:
            # Disconnect
            self.stop_thread.set()
            if self.read_thread:
                self.read_thread.join()
            self.serial_port.close()
            self.serial_port = None
            self.connect_button.config(text="Connect", bootstyle="success")
            self.root.update_idletasks()  # Ensure GUI updates before playing the sound
            self.play_sound("disconnect_sound.wav")  # Add sound for disconnection
        else:
            if not self.port_var.get():
                messagebox.showerror("Error", "Please select a COM port before connecting.")
                return
            try:
                # Connect
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
                self.play_sound("connect_sound.wav")  # Add sound for connection
            except serial.SerialException as e:
                messagebox.showerror("Error", str(e))

    def export_data(self):
        """Export received data to a file."""
        # Open a save file dialog
        filetypes = [("Text File", "*.txt"), ("CSV File", "*.csv"), ("JSON File", "*.json")]
        filepath = filedialog.asksaveasfilename(title="Save Data", defaultextension=".txt", filetypes=filetypes)

        if filepath:
            try:
                # Get the received data
                self.receive_text.config(state=NORMAL)  # Temporarily enable editing to get content
                data = self.receive_text.get(1.0, "end-1c")  # Get all text except the trailing newline
                self.receive_text.config(state=DISABLED)  # Disable editing again

                # Write data to the selected file format
                if filepath.endswith(".txt"):
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(data)

                elif filepath.endswith(".csv"):
                    with open(filepath, "w", encoding="utf-8") as f:
                        lines = data.split("\n")
                        f.write("Timestamp,Message\n")  # Example CSV header
                        for line in lines:
                            if line.strip():  # Skip empty lines
                                timestamp, message = self.parse_line(line)
                                f.write(f"{timestamp},{message}\n")

                elif filepath.endswith(".json"):
                    with open(filepath, "w", encoding="utf-8") as f:
                        lines = data.split("\n")
                        json_data = [{"timestamp": self.parse_line(line)[0], "message": self.parse_line(line)[1]} for line in lines if line.strip()]
                        json.dump(json_data, f, indent=4)

                messagebox.showinfo("Export Success", f"Data exported successfully to {filepath}")

            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export data: {e}")

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
        if self.save_timestamp.get():  # Check if timestamps are enabled
            timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
            formatted_data = f"{timestamp} {data}"  # Add timestamp to the data
        else:
            formatted_data = data

        self.receive_text.config(state=NORMAL)
        self.receive_text.insert("end", formatted_data)
        self.receive_text.see("end")  # Auto-scroll to the end
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
                elif eol == "Other":
                    message += self.custom_eol_var.get()  # Use custom EOL input
                # Send the message
                self.serial_port.write(message.encode('utf-8'))
        else:
            messagebox.showerror("Error", "Serial port is not connected.")

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
