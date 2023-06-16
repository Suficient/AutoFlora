import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import urllib.request
import cv2
import os
import glob
import re
from PIL import Image, ImageTk
import tkinter.messagebox
import csv
from datetime import datetime
import subprocess

#subprocesses to be run
# import heatmap
import disease_predictor
import esp32camphotosaver


# Function to generate matplotlib graphs
def generate_graphs():
    pass


# Function to get the most recent image with a certain word at the beginning of its file name
def get_recent_image():
    folder_path = 'C:/Users/Faizan Tabassum/Desktop/GardenWatch/ESPphotos'
    healthyword = 'healthy'
    unhealthyword = 'unhealthy'
    file_list = glob.glob(os.path.join(folder_path, f'*.jpeg'))  
    if file_list:
        file_list.sort(key=os.path.getctime)
        recent_image_path = file_list[-1]
        if recent_image_path == 'healthy':
            status = 'healthy'
        elif recent_image_path == 'unhealthy':
            status = 'unhealthy'
        else: return None
        return status,recent_image_path
    else:
        return None

    # Sort files by creation time and get the most recent one
    
temptup = get_recent_image()

print(temptup)

# Set up the GUI
root = tk.Tk()
root.title("ESP32 Cam Live Feed")

# Set up the list of ESP32 cam IP addresses
ip_addresses = "http://192.168.236.243",
current_ip_address_index = 0

# Set up the video capture from the current ESP32 cam
url = ip_addresses[current_ip_address_index]
stream = urllib.request.urlopen(url)
bytes = bytes()

# Define a function to update the video feed
def update_video_feed():
    global bytes, current_ip_address_index
    bytes += stream.read(1024)
    a = bytes.find(b'\xff\xd8')
    b = bytes.find(b'\xff\xd9')
    if a != -1 and b != -1:
        jpg = bytes[a:b+2]
        bytes = bytes[b+2:]
        frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        video_feed_label.imgtk = imgtk
        video_feed_label.configure(image=imgtk)
    root.after(10, update_video_feed)

# Define a function to switch to the next ESP32 cam IP address
def switch_to_next_ip_address():
    global url, stream, bytes, current_ip_address_index
    current_ip_address_index = (current_ip_address_index + 1) % len(ip_addresses)
    url = ip_addresses[current_ip_address_index]
    stream = urllib.request.urlopen(url)
    bytes = bytes()
    root.after(10000, switch_to_next_ip_address)



# Define a function to detect disease
def detect_disease():
    cv2.imread()
    output_box.insert(tk.END, "Disease detected!\n")

# Set up the video feed label
video_feed_label = tk.Label(root)
video_feed_label.pack()

# Set up the "Plot Graph" button
plot_graph_button = tk.Button(root, text="Plot Graph", command=plot_graph)
plot_graph_button.pack(side=tk.LEFT)

# Set up the "Detect Disease" button and output box
detect_disease_button = tk.Button(root, text="Detect Disease", command=detect_disease)
detect_disease_button.pack(side=tk.LEFT)
output_box = tk.Text(root, height=2, width=30)
output_box.pack(side=tk.LEFT)

# Start the video feed update loop
update_video_feed()

# Start the GUI
root.mainloop()

# Generate the graphs
graph1, graph2, graph3 = generate_graphs()

# Create a canvas to display the graphs
canvas = FigureCanvasTkAgg(graph1, master=root)
canvas.get_tk_widget().grid(row=0, column=0)

# Create buttons to switch between graphs
graph_frames = [graph1, graph2, graph3]
current_graph_index = 0


def switch_graph(forward=True):
    global current_graph_index
    if forward:
        current_graph_index = (current_graph_index + 1) % len(graph_frames)
    else:
        current_graph_index = (current_graph_index - 1) % len(graph_frames)
    canvas.figure = graph_frames[current_graph_index]
    canvas.draw()


btn_prev = tk.Button(root, text='<< Prev', command=lambda: switch_graph(forward=False))
btn_prev.grid(row=1, column=0, sticky='w')

btn_next = tk.Button(root, text='Next >>', command=lambda: switch_graph(forward=True))
btn_next.grid(row=1, column=0, sticky='e')

#
