import serial
import threading
from tkinter import *
from tkinter import ttk
import time

def send(*args):
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

def rotate_cw_90():
    send_command("M90")

def rotate_ccw_90():
    send_command("N90")

def send_command(command):
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
root.configure(bg="#0077be")

mainframe = ttk.Frame(root, padding="3 3 12 12", style="My.TFrame")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

style = ttk.Style()
style.configure("My.TFrame", background="#0077be")

rpm = StringVar()
degree = StringVar()
direc = StringVar()
pos = IntVar()
status_text = StringVar()

feet_entry = ttk.Entry(mainframe, width=7, textvariable=rpm)
feet_entry.grid(column=2, row=1, sticky=(W, E))
degree_entry = ttk.Entry(mainframe, width=7, textvariable=degree)
degree_entry.grid(column=7, row=1, sticky=(W, E))

ttk.Label(mainframe, textvariable=pos).grid(column=2, row=3, sticky=(W, E))

box = ttk.Combobox(mainframe, textvariable=direc, state='readonly')
box['values'] = ('CW', 'CCW')
box.current(0)
box.grid(column=5, row=1, sticky=(E))

btn = ttk.Button(mainframe, text="Send", command=send)
btn.grid(column=8, row=4, sticky=W)

status_button = ttk.Button(mainframe, text="Arduino Status", command=receive_status)
status_button.grid(column=8, row=5, sticky=W)

reset_button = ttk.Button(mainframe, text="Reset Motor", command=reset_motor)
reset_button.grid(column=8, row=6, sticky=W)

cw_button = ttk.Button(mainframe, text="CW 90", command=rotate_cw_90)
cw_button.grid(column=6, row=4, sticky=W)

ccw_button = ttk.Button(mainframe, text="CCW 90", command=rotate_ccw_90)
ccw_button.grid(column=7, row=4, sticky=W)

status_label = ttk.Label(mainframe, textvariable=status_text)
status_label.grid(column=2, row=5, columnspan=3, sticky=(W, E))

ttk.Label(mainframe, text="Speed").grid(column=1, row=1, sticky=W)
ttk.Label(mainframe, text="rpm").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="Direction").grid(column=4, row=1, sticky=W)
ttk.Label(mainframe, text="Angle").grid(column=6, row=1, sticky=E)
ttk.Label(mainframe, text="degree").grid(column=8, row=1, sticky=E)
ttk.Label(mainframe, text="Value").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="rpm").grid(column=3, row=2, sticky=W)
ttk.Label(mainframe, text="Value").grid(column=1, row=3, sticky=E)
ttk.Label(mainframe, text="Degree").grid(column=3, row=3, sticky=W)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()
