from tkinter import *
from PIL import ImageTk, Image
import serial
import time
import math


root = Tk()
root.geometry('1200x600')
root.configure(bg='#273238')

# Frame definitions
map_frame = Frame(root, width=600, height=600, bg='#273238')
data_frame = Frame(root, width=600, height=600, bg='#273238')
control_telemetry_frame = Frame(data_frame, width=600, height=300, bg='#273238')
widgets_console_frame = Frame(data_frame, width=600, height=300, bg='#273238')
control_frame = Frame(control_telemetry_frame, width=290, height=285, bg='#303f46')
telemetry_frame = Frame(control_telemetry_frame, width=290, height=285, bg='#303f46')
widgets_frame = Frame(widgets_console_frame, width=585, height=140, bg='#303f46')
console_frame = Frame(widgets_console_frame, width=585, height=140, bg='#303f46')

# Disable frame auto scaling
map_frame.pack_propagate(False)
data_frame.pack_propagate(False)
control_telemetry_frame.pack_propagate(False)
widgets_console_frame.pack_propagate(False)
control_frame.grid_propagate(False)
telemetry_frame.grid_propagate(False)
widgets_frame.grid_propagate(False)
console_frame.grid_propagate(False)

# Frame placements
map_frame.pack(side='left')
data_frame.pack(side='right')
control_telemetry_frame.pack(side='top')
widgets_console_frame.pack(side='bottom')
control_frame.pack(side='left', padx=(5, 5), pady=(10, 5))
telemetry_frame.pack(side='right', padx=(5, 10), pady=(10, 5))
widgets_frame.pack(side='top', padx=(5, 10), pady=(5, 5))
console_frame.pack(side='bottom', padx=(5, 10), pady=(5, 10))

# Map frame
map_canvas = Canvas(map_frame, width=580, height=580, highlightthickness=0)

map_image = Image.open('assets/map_temp.png')
map_canvas.image = ImageTk.PhotoImage(map_image.resize((600, 600), Image.ANTIALIAS))
map_canvas.create_image(0, 0, image=map_canvas.image, anchor='nw')

boat_image = PhotoImage(file='assets/boat.png')
map_canvas.create_image(300, 300, image=boat_image)

# Map placements
map_canvas.pack(padx=(10, 5), pady=(10, 10))

# Control frame
control_label = Label(control_frame, text="Control Signal", fg='#bbbbbb', bg='#303f46')
auto_label = Label(control_frame, text="Auto (enable/disable): ", fg='#aaaaaa', bg='#303f46')
max_speed_label = Label(control_frame, text="Max speed (ppm): ", fg='#aaaaaa', bg='#303f46')
cruise_speed_label = Label(control_frame, text="Cruise speed (ppm): ", fg='#aaaaaa', bg='#303f46')
desired_heading_label = Label(control_frame, text="Desired heading (degree): ", fg='#aaaaaa', bg='#303f46')
kp_label = Label(control_frame, text="Kp (float): ", fg='#aaaaaa', bg='#303f46')
ki_label = Label(control_frame, text="Ki (float): ", fg='#aaaaaa', bg='#303f46')
kd_label = Label(control_frame, text="Kd (float): ", fg='#aaaaaa', bg='#303f46')
update_interval_label = Label(control_frame, text="Update interval (ms): ", fg='#aaaaaa', bg='#303f46')

auto_var = StringVar(control_frame, value="0")
max_speed_var = StringVar(control_frame, value="1500")
cruise_speed_var = StringVar(control_frame, value="1000")
desired_heading_var = StringVar(control_frame, value="90")
kp_var = StringVar(control_frame, value="5")
ki_var = StringVar(control_frame, value="0")
kd_var = StringVar(control_frame, value="0")
update_interval_var = StringVar(control_frame, value="500")

auto_entry = Entry(control_frame, textvariable=auto_var, width=10)
max_speed_entry = Entry(control_frame, textvariable=max_speed_var, width=10)
cruise_speed_entry = Entry(control_frame, textvariable=cruise_speed_var, width=10)
desired_heading_entry = Entry(control_frame, textvariable=desired_heading_var, width=10)
kp_entry = Entry(control_frame, textvariable=kp_var, width=10)
ki_entry = Entry(control_frame, textvariable=ki_var, width=10)
kd_entry = Entry(control_frame, textvariable=kd_var, width=10)
update_interval_entry = Entry(control_frame, textvariable=update_interval_var, width=10)

auto_entry.configure({'background': '#273238'})
auto_entry.configure({'foreground': '#aaaaaa'})
max_speed_entry.configure({'background': '#273238'})
max_speed_entry.configure({'foreground': '#aaaaaa'})
cruise_speed_entry.configure({'background': '#273238'})
cruise_speed_entry.configure({'foreground': '#aaaaaa'})
desired_heading_entry.configure({'background': '#273238'})
desired_heading_entry.configure({'foreground': '#aaaaaa'})
kp_entry.configure({'background': '#273238'})
kp_entry.configure({'foreground': '#aaaaaa'})
ki_entry.configure({'background': '#273238'})
ki_entry.configure({'foreground': '#aaaaaa'})
kd_entry.configure({'background': '#273238'})
kd_entry.configure({'foreground': '#aaaaaa'})
update_interval_entry.configure({'background': '#273238'})
update_interval_entry.configure({'foreground': '#aaaaaa'})

def auto_callback():
    if auto_var.get() == "0":
        receiver.write("S\n".encode('utf-8'))
    else:
        receiver.write("s\n".encode('utf-8'))

def max_speed_callback():
    command = f'm{max_speed_var.get()}\n'
    receiver.write(command.encode('utf-8'))

def cruise_speed_callback():
    command = f'c{cruise_speed_var.get()}\n'
    receiver.write(command.encode('utf-8'))

def desired_heading_callback():
    command = f'h{desired_heading_var.get()}\n'
    receiver.write(command.encode('utf-8'))

def kp_callback():
    command = f'p{kp_var.get()}\n'
    receiver.write(command.encode('utf-8'))

def ki_callback():
    command = f'i{ki_var.get()}\n'
    receiver.write(command.encode('utf-8'))

def kd_callback():
    command = f'd{kd_var.get()}\n'
    receiver.write(command.encode('utf-8'))

auto_button = Button(control_frame, text="Send", bg='#273238', fg='#aaaaaa', command=auto_callback)
max_speed_button = Button(control_frame, text="Send", bg='#273238', fg='#aaaaaa', command=max_speed_callback)
cruise_speed_button = Button(control_frame, text="Send", bg='#273238', fg='#aaaaaa', command=cruise_speed_callback)
desired_heading_button = Button(control_frame, text="Send", bg='#273238', fg='#aaaaaa', command=desired_heading_callback)
kp_button = Button(control_frame, text="Send", bg='#273238', fg='#aaaaaa', command=kp_callback)
ki_button = Button(control_frame, text="Send", bg='#273238', fg='#aaaaaa', command=ki_callback)
kd_button = Button(control_frame, text="Send", bg='#273238', fg='#aaaaaa', command=kd_callback)
update_interval_button = Button(control_frame, text="Send", bg='#273238', fg='#aaaaaa')

# Control placements
control_label.grid(row=0, column=0, sticky='w', pady=2)
auto_label.grid(row=1, column=0, sticky='w', pady=2)
max_speed_label.grid(row=2, column=0, sticky='w', pady=2)
cruise_speed_label.grid(row=3, column=0, sticky='w', pady=2)
desired_heading_label.grid(row=4, column=0, sticky='w', pady=2)
kp_label.grid(row=5, column=0, sticky='w', pady=2)
ki_label.grid(row=6, column=0, sticky='w', pady=2)
kd_label.grid(row=7, column=0, sticky='w', pady=2)
update_interval_label.grid(row=8, column=0, sticky='w', pady=2)

auto_entry.grid(row=1, column=1, sticky='w', pady=2)
max_speed_entry.grid(row=2, column=1, sticky='w', pady=2)
cruise_speed_entry.grid(row=3, column=1, sticky='w', pady=2)
desired_heading_entry.grid(row=4, column=1, sticky='w', pady=2)
kp_entry.grid(row=5, column=1, sticky='w', pady=2)
ki_entry.grid(row=6, column=1, sticky='w', pady=2)
kd_entry.grid(row=7, column=1, sticky='w', pady=2)
update_interval_entry.grid(row=8, column=1, sticky='w', pady=2)

auto_button.grid(row=1, column=3, pady=2, padx=30)
max_speed_button.grid(row=2, column=3, pady=2, padx=30)
cruise_speed_button.grid(row=3, column=3, pady=2, padx=30)
desired_heading_button.grid(row=4, column=3, pady=2, padx=30)
kp_button.grid(row=5, column=3, pady=2, padx=30)
ki_button.grid(row=6, column=3, pady=2, padx=30)
kd_button.grid(row=7, column=3, pady=2, padx=30)
update_interval_button.grid(row=8, column=3, pady=2, padx=30)

# Telemetry frame
telemetry_label = Label(telemetry_frame, text="Telemetry Signal", fg='#bbbbbb', bg='#303f46')
mode_label = Label(telemetry_frame, text="Mode: ", fg='#aaaaaa', bg='#303f46')
throttle_label = Label(telemetry_frame, text="Throttle (ppm): ", fg='#aaaaaa', bg='#303f46')
rudder_label = Label(telemetry_frame, text="Rudder (ppm): ", fg='#aaaaaa', bg='#303f46')
left_motor_speed_label = Label(telemetry_frame, text="Left motor speed (ppm): ", fg='#aaaaaa', bg='#303f46')
right_motor_speed_label = Label(telemetry_frame, text="Right motor speed (ppm): ", fg='#aaaaaa', bg='#303f46')
current_heading_label = Label(telemetry_frame, text="Current heading (degrees): ", fg='#aaaaaa', bg='#303f46')
lat_label = Label(telemetry_frame, text="Latitude (float): ", fg='#aaaaaa', bg='#303f46')
lon_label = Label(telemetry_frame, text="Longitude (float): ", fg='#aaaaaa', bg='#303f46')
cell1_label = Label(telemetry_frame, text="Cell1 voltage (volt): ", fg='#aaaaaa', bg='#303f46')
cell2_label = Label(telemetry_frame, text="Cell2 voltage (volt): ", fg='#aaaaaa', bg='#303f46')
cell3_label = Label(telemetry_frame, text="Cell3 voltage (volt): ", fg='#aaaaaa', bg='#303f46')

mode_var = StringVar(telemetry_frame, value="manual")
throttle_var = StringVar(telemetry_frame, value="1000")
rudder_var = StringVar(telemetry_frame, value="1500")
left_motor_speed_var = StringVar(telemetry_frame, value="1000")
right_motor_speed_var = StringVar(telemetry_frame, value="1000")
current_heading_var = StringVar(telemetry_frame, value="0")
lat_var = StringVar(telemetry_frame, value="1.0")
lon_var = StringVar(telemetry_frame, value="1.0")
cell1_var = StringVar(telemetry_frame, value="3.75")
cell2_var = StringVar(telemetry_frame, value="3.82")
cell3_var = StringVar(telemetry_frame, value="3.76")

mode_display = Label(telemetry_frame, textvariable=mode_var, fg='#bbbbbb', bg='#303f46')
throttle_display = Label(telemetry_frame, textvariable=throttle_var, fg='#bbbbbb', bg='#303f46')
rudder_display = Label(telemetry_frame, textvariable=rudder_var, fg='#bbbbbb', bg='#303f46')
left_motor_speed_display = Label(telemetry_frame, textvariable=left_motor_speed_var, fg='#bbbbbb', bg='#303f46')
right_motor_speed_display = Label(telemetry_frame, textvariable=right_motor_speed_var, fg='#bbbbbb', bg='#303f46')
current_heading_display = Label(telemetry_frame, textvariable=current_heading_var, fg='#bbbbbb', bg='#303f46')
lat_display = Label(telemetry_frame, textvariable=lat_var, fg='#bbbbbb', bg='#303f46')
lon_display = Label(telemetry_frame, textvariable=lon_var, fg='#bbbbbb', bg='#303f46')
cell1_display = Label(telemetry_frame, textvariable=cell1_var, fg='#bbbbbb', bg='#303f46')
cell2_display = Label(telemetry_frame, textvariable=cell2_var, fg='#bbbbbb', bg='#303f46')
cell3_display = Label(telemetry_frame, textvariable=cell3_var, fg='#bbbbbb', bg='#303f46')

# Telemetry placements
telemetry_label.grid(row=0, column=0, pady=1)
mode_label.grid(row=1, column=0, sticky='w', pady=1)
throttle_label.grid(row=2, column=0, sticky='w', pady=1)
rudder_label.grid(row=3, column=0, sticky='w', pady=1)
left_motor_speed_label.grid(row=4, column=0, sticky='w', pady=1)
right_motor_speed_label.grid(row=5, column=0, sticky='w', pady=1)
current_heading_label.grid(row=6, column=0, sticky='w', pady=1)
lat_label.grid(row=7, column=0, sticky='w', pady=1)
lon_label.grid(row=8, column=0, sticky='w', pady=1)
cell1_label.grid(row=9, column=0, sticky='w', pady=1)
cell2_label.grid(row=10, column=0, sticky='w', pady=1)
cell3_label.grid(row=11, column=0, sticky='w', pady=1)

mode_display.grid(row=1, column=1, sticky='w')
throttle_display.grid(row=2, column=1, sticky='w')
rudder_display.grid(row=3, column=1, sticky='w')
left_motor_speed_display.grid(row=4, column=1, sticky='w')
right_motor_speed_display.grid(row=5, column=1, sticky='w')
current_heading_display.grid(row=6, column=1, sticky='w')
lat_display.grid(row=7, column=1, sticky='w')
lon_display.grid(row=8, column=1, sticky='w')
cell1_display.grid(row=9, column=1, sticky='w')
cell2_display.grid(row=10, column=1, sticky='w')
cell3_display.grid(row=11, column=1, sticky='w')

# Widgets frame
widgets_label = Label(widgets_frame, text="Widgets", fg='#bbbbbb', bg='#303f46')

# Widgets placements
widgets_label.grid(row=0, column=0)

# Console frame
console_label = Label(console_frame, text="Debug Console", fg='#bbbbbb', bg='#303f46')

debug_message_var = StringVar(console_frame)

debug_message_display = Label(console_frame, textvariable=debug_message_var, fg='#bbbbbb', bg='#303f46')

# Console placements
console_label.grid(row=0, column=0, sticky='w')

debug_message_display.grid(row=1, column=0, sticky='w', pady=40)

line1ID = None
line2ID = None

def update_map(values):
    global line1ID
    global line2ID
    
    map_canvas.delete(line1ID)
    map_canvas.delete(line2ID)

    desired_heading_angle = int(desired_heading_var.get())
    current_heading_angle = int(values[5])
    
    line1ID = map_canvas.create_line(300, 300, 300+1000*math.cos(math.radians(90-desired_heading_angle)), 300-1000*math.sin(math.radians(90-desired_heading_angle)), fill='#2398f5', width=2)
    line2ID = map_canvas.create_line(300, 300, 300+1000*math.cos(math.radians(90-current_heading_angle)), 300-1000*math.sin(math.radians(90-current_heading_angle)), fill='#e3be00', width=2)

def update_telemetry(values):
    if values[0] == '0':
        mode_var.set("Manual")
    else:
        mode_var.set("Auto")

    throttle_var.set(values[1])
    rudder_var.set(values[2])
    left_motor_speed_var.set(values[3])
    right_motor_speed_var.set(values[4])
    current_heading_var.set(values[5])
    lat_var.set(values[6])
    lon_var.set(values[7])
    cell1_var.set(values[8])
    cell2_var.set(values[9])
    cell3_var.set(values[10])
    
def update_debug_console(line):
    debug_message_var.set(line)

#receiver = serial.Serial('COM4', 9600, timeout=0.1)
time.sleep(2)
loop = True

while loop:
    root.update()
    #line = receiver.readline()
    #line = line.decode("utf-8").rstrip()
    # print(line)
##    if (line[0:11] == "[TELEMETRY]"):
##        values = line[12:].split("\t")
##        update_telemetry(values)
##        update_map(values)
##    elif (line[0:7] == "[ERROR]"):
##        update_debug_console(line)

