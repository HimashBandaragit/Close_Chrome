import time
import os
import platform
import threading
import tkinter as tk
from tkinter import messagebox

# Global variables
countdown_active = False  
time_left = 3600  # Default to 1 hour

# Function to close Google Chrome
def close_chrome():
    system = platform.system()
    
    if system == "Windows":
        os.system("taskkill /F /IM chrome.exe")
    elif system == "Linux":
        os.system("pkill chrome")
    elif system == "Darwin":  # macOS
        os.system("pkill -f 'Google Chrome'")

# Countdown function
def start_countdown():
    global countdown_active, time_left
    countdown_active = True  
    seconds = int(time_left)  # Get time from slider

    def countdown():
        for i in range(seconds, 0, -1):  
            if not countdown_active:  
                timer_label.config(text="Countdown Stopped")
                return
            
            hrs, mins, secs = i // 3600, (i % 3600) // 60, i % 60
            timer_label.config(text=f"Time Left: {hrs:02}:{mins:02}:{secs:02}")
            time.sleep(1)

        timer_label.config(text="Closing Chrome...")
        close_chrome()
        messagebox.showinfo("Chrome Closed", "Google Chrome has been closed.")

    # Run countdown in a separate thread to keep UI responsive
    thread = threading.Thread(target=countdown)
    thread.start()

# Function to stop countdown
def stop_countdown():
    global countdown_active
    countdown_active = False  

# Function to update selected time from slider
def update_time(val):
    global time_left
    time_left = int(float(val) * 3600)  # Convert hours to seconds
    hrs, mins, secs = int(float(val)), 0, 0
    timer_label.config(text=f"Selected Time: {hrs:02}:{mins:02}:{secs:02}")

# Create GUI Window
root = tk.Tk()
root.title("Chrome Auto Closer")
root.geometry("400x300")

# UI Elements
label = tk.Label(root, text="Set time before Chrome closes:", font=("Arial", 12))
label.pack(pady=5)

# Time slider (0.1 to 24 hours)
time_slider = tk.Scale(root, from_=0.1, to=24, resolution=0.1, orient="horizontal", length=300, command=update_time)
time_slider.set(1)  # Default to 1 hour
time_slider.pack(pady=5)

timer_label = tk.Label(root, text="Selected Time: 01:00:00", font=("Arial", 14), fg="blue")
timer_label.pack(pady=10)

start_button = tk.Button(root, text="Start Countdown", font=("Arial", 12), command=start_countdown)
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop Countdown", font=("Arial", 12), fg="white", bg="red", command=stop_countdown)
stop_button.pack(pady=5)

# Run UI
root.mainloop()
