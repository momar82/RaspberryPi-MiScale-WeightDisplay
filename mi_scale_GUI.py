import tkinter as tk
from tkinter import ttk
import threading
from miScale import MiScale
import time

def on_data_received(scale):
    # Update the label text with the received weight
    weight = scale.weight
    weight_label.config(text="Weight: {} kg".format(weight))
    
    # Change label background color based on weight
    if weight > 15:
        weight_label.config(bg="red")
    else:
        weight_label.config(bg="green")

def start_mi_scale():
    global mi_scale
    while True:
        try:
            mi_scale = MiScale(mac_addr, on_data_received, send_only_stabilized_weight)
            mi_scale.start()
            break  # Exit the loop if successful
        except Exception as e:
            # Retry after a delay if an error occurs
            time.sleep(1)  # Adjust delay as needed

def run_mi_scale():
    # Start MiScale initialization in a separate thread
    mi_scale_thread = threading.Thread(target=start_mi_scale)
    mi_scale_thread.daemon = True
    mi_scale_thread.start()

mac_addr = "5C:64:F3:42:7D:F1"  # Replace with your device's MAC address
send_only_stabilized_weight = False  # Change to True if desired

# Create the main Tkinter window
root = tk.Tk()
root.title("Mi Scale Weight Display")

# Set window size to maximum
root.attributes('-zoomed', True)

# Create a label to display the weight
weight_label = tk.Label(root, text="Weight: -- kg", font=("Arial", 50), bg="green")
weight_label.pack(pady=20)

# Create a toolbar
toolbar = ttk.Frame(root)
toolbar.pack(side="top", fill="x")

# Add a button to the toolbar to run MiScale initialization
run_button = ttk.Button(toolbar, text="Run MiScale", command=run_mi_scale)
run_button.pack(side="left", padx=5, pady=5)

# Start the Tkinter event loop
root.mainloop()
