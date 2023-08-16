import tkinter as tk
import serial
import queue
import threading
import time

class DaminGUI:
    def __init__(self, root, command_queue):
        self.root = root
        self.command_queue = command_queue

        self.root.title("Stepper Motor Control")
        self.root.geometry("400x400")
        self.root.configure(bg="#800000")

        self.connection_status = tk.Label(self.root, text="Arduino Not Connected", fg="red")
        self.connection_status.pack()

        self.create_buttons()

    def create_buttons(self):
        cw_button = tk.Button(self.root, text="CW (30 deg)", command=self.send_cw_command)
        cw_button.pack()

        ccw_button = tk.Button(self.root, text="CCW (30 deg)", command=self.send_ccw_command)
        ccw_button.pack()

        stop_button = tk.Button(self.root, text="Stop", command=self.send_stop_command)
        stop_button.pack()

        get_status_button = tk.Button(self.root, text="Get Status", command=self.send_get_status_command)
        get_status_button.pack()

    def send_cw_command(self):
        self.command_queue.put("CW")

    def send_ccw_command(self):
        self.command_queue.put("CCW")

    def send_stop_command(self):
        self.command_queue.put("STOP")

    def send_get_status_command(self):
        self.command_queue.put("GET_STATUS")

def control_motor(command_queue):
    try:
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        gui.connection_status.pack_forget() 
    except serial.SerialException:
        ser = None  # Arduino not connected

    while True:
        if ser:
            try:
                command = command_queue.get(timeout=0.1)  # From the queue
                ser.write(command.encode())
                print(f"Sent command: {command}")
                time.sleep(0.1)  # Give Arduino some buffer time

                if command == "GET_STATUS":
                    arduinoResponse = ser.readline().decode().strip()
                    print(f"Received status: {arduinoResponse}")
            except queue.Empty:
                pass  # Continue waiting if Queue is empty
        else:
            print("Arduino not connected")

if __name__ == "__main__":
    command_queue = queue.Queue()

    root = tk.Tk()
    gui = DaminGUI(root, command_queue)

    motor_thread = threading.Thread(target=control_motor, args=(command_queue,))
    motor_thread.start()

    root.mainloop()
