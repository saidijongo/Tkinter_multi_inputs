import serial
import threading
from tkinter import *
from tkinter import ttk
import time

def send(*args):
    def send_thread():
        try:
            data = rpm.get() + direc.get() + degree.get()
            global pos
            pos.set(pos.get() + int(degree.get()))
            print(data)

            ser = serial.Serial('/dev/ttyUSB0', 9600)
            time.sleep(2)
            ser.write(data.encode())
            time.sleep(5)

            while True:
                myData = ''
                if ser.inWaiting() > 0:
                    myData = ser.readline()
                    print(myData.decode())
                if myData == "":
                    break

            ser.close()
        except ValueError:
            pass

    send_thread = threading.Thread(target=send_thread)
    send_thread.start()

def rotate_cw_90():
    send_command("CW90")

def rotate_ccw_90():
    send_command("CCW90")

def send_command(command):
    def command_thread():
        try:
            ser = serial.Serial('/dev/ttyUSB0', 9600)
            ser.write(command.encode())
            time.sleep(0.5)
            response = ser.readline().decode().strip()
            ser.close()

            if response == "Done":
                status_text.set("Arduino Status: Motor rotated 90 degrees")
            else:
                status_text.set("Arduino Status: Error")
        except:
            status_text.set("Arduino Status: Error")

    command_thread = threading.Thread(target=command_thread)
    command_thread.start()

def receive_status():
    def status_thread():
        try:
            ser = serial.Serial('/dev/ttyUSB0', 9600)
            ser.write(b'S')
            time.sleep(0.5)
            status = ser.readline().decode().strip()
            ser.close()

            if status:
                status_text.set(f"Arduino Status: {status}")
            else:
                status_text.set("Arduino Status: No response")
        except:
            status_text.set("Arduino Status: Error")

    status_thread = threading.Thread(target=status_thread)
    status_thread.start()

def reset_motor():
    def reset_thread():
        try:
            ser = serial.Serial('/dev/ttyUSB0', 9600)
            ser.write(b'R')
            time.sleep(0.5)
            ser.close()
            pos.set(0)
            status_text.set("Arduino Status: Motor reset")
        except:
            status_text.set("Arduino Status: Error")

    reset_thread = threading.Thread(target=reset_thread)
    reset_thread.start()

root = Tk()
root.title("Stepper Motor Control")
root.configure(bg="red")

# Define variables
rpm = StringVar()
degree = StringVar()
direc = StringVar()
pos = IntVar()
status_text = StringVar()

# Create mainframes to separate sections
input_frame = ttk.Frame(root, style="My.TFrame")
input_frame.grid(column=0, row=0, sticky=(N, W, E))
output_frame = ttk.Frame(root, style="My.TFrame")
output_frame.grid(column=0, row=1, sticky=(N, W, E))

style = ttk.Style()
style.configure("My.TFrame", background="red")

# Input section
ttk.Label(input_frame, text="Speed").grid(column=1, row=1, sticky=W)
ttk.Label(input_frame, text="rpm").grid(column=3, row=1, sticky=W)
ttk.Label(input_frame, text="Direction").grid(column=4, row=1, sticky=W)
ttk.Label(input_frame, text="Angle").grid(column=6, row=1, sticky=E)
ttk.Label(input_frame, text="degree").grid(column=8, row=1, sticky=E)

feet_entry = ttk.Entry(input_frame, width=7, textvariable=rpm)
feet_entry.grid(column=2, row=1, sticky=(W, E))
degree_entry = ttk.Entry(input_frame, width=7, textvariable=degree)
degree_entry.grid(column=7, row=1, sticky=(W, E))
box = ttk.Combobox(input_frame, textvariable=direc, state='readonly')
box['values'] = ('CW', 'CCW')
box.current(0)
box.grid(column=5, row=1, sticky=(E))
send_button = ttk.Button(input_frame, text="Send", command=send)
send_button.grid(column=8, row=2, sticky=W)

# Separator line
separator = ttk.Separator(root, orient="horizontal")
separator.grid(column=0, row=2, sticky=(W, E), pady=10)

# Output section
status_label = ttk.Label(output_frame, textvariable=status_text)
status_label.grid(column=2, row=0, columnspan=2, sticky=(W, E))

status_button = ttk.Button(output_frame, text="Arduino Status", command=receive_status)
status_button.grid(column=2, row=1, sticky=W)

reset_button = ttk.Button(output_frame, text="Reset Motor", command=reset_motor)
reset_button.grid(column=3, row=1, sticky=W)

cw_button = ttk.Button(output_frame, text="CW 90", command=rotate_cw_90)
cw_button.grid(column=2, row=2, sticky=W)

ccw_button = ttk.Button(output_frame, text="CCW 90", command=rotate_ccw_90)
ccw_button.grid(column=3, row=2, sticky=W)

for child in input_frame.winfo_children():
    child.grid_configure(padx=5, pady=5)

for child in output_frame.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()
