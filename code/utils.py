# utils.py
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import threading
import time
import shutil
from tracker import run_video_summarization
# Constants
forest_green = '#00897B'

# Global variables
selected_video_path = ""
selected_classes = []
is_playing = False
is_paused = False
is_stopped = False
is_summarizing = False

# Widgets to be initialized in main.py
progress_bar = None
download_btn = None
video_label = None
video_title_label = None

coco_classes = [
    "Person", "Bicycle", "Car", "Motorcycle", "Airplane",
    "Bus", "Train", "Truck", "Boat", "Traffic light",
    "Fire hydrant", "Stop sign", "Parking meter", "Bench",
    "Bird", "Cat", "Dog", "Horse", "Sheep", "Cow",
    "Elephant", "Bear", "Zebra", "Giraffe", "Backpack",
    "Umbrella", "Handbag", "Tie", "Suitcase", "Frisbee",
    "Skis", "Snowboard", "Sports ball", "Kite", "Baseball bat",
    "Baseball glove", "Skateboard", "Surfboard", "Tennis racket", "Bottle",
    "Wine glass", "Cup", "Fork", "Knife", "Spoon",
    "Bowl", "Banana", "Apple", "Sandwich", "Orange",
    "Broccoli", "Carrot", "Hot dog", "Pizza", "Donut",
    "Cake", "Chair", "Couch", "Potted plant", "Bed",
    "Dining table", "Toilet", "TV", "Laptop", "Mouse",
    "Remote", "Keyboard", "Cell phone", "Microwave", "Oven",
    "Toaster", "Sink", "Refrigerator", "Book", "Clock",
    "Vase", "Scissors", "Teddy bear", "Hair drier", "Toothbrush"
]



def on_class_selection(event):
    global selected_classes
    selected_classes = [event.widget.get()] if event.widget.get() else []

def on_video_label_click(event):
    play_video_handler()

def play_video(video_path):
    global is_playing, is_paused, is_stopped
    if not video_path:
        print("Video path is empty.")
        return
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Failed to open video.")
        return
    target_size = (500, 500)
    while cap.isOpened() and not is_stopped:
        if is_paused:
            time.sleep(0.1)
            continue
        ret, frame = cap.read()
        if ret and is_playing:
            display_frame(frame)
        elif not ret:
            break
    cap.release()
    reset_video_controls()

def display_frame(frame):
    target_size = (500, 500)
    (height, width) = frame.shape[:2]
    scale = min(target_size[0] / width, target_size[1] / height)
    dim = (int(width * scale), int(height * scale))
    frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    im = Image.fromarray(frame)
    img = ImageTk.PhotoImage(image=im)
    video_label.config(image=img)
    video_label.image = img
    video_label.update()

def play_video_handler():
    global is_playing, is_paused, is_stopped
    is_playing = True
    is_paused = False
    is_stopped = False
    threading.Thread(target=play_video, args=(selected_video_path,), daemon=True).start()

def pause_video():
    global is_paused
    is_paused = True

def stop_video():
    global is_stopped
    is_stopped = True

def reset_video_controls():
    global is_playing, is_paused, is_stopped
    is_playing = False
    is_paused = False
    is_stopped = False
def upload_video(root):
    allowed_formats = [("MP4 files", "*.mp4"), ("AVI files", "*.avi")]
    filepath = filedialog.askopenfilename(title="Select file", filetypes=allowed_formats)
    if filepath:
        progress_bar['value'] = 0  # Reset the progress bar immediately after a new file is selected
        video_title_label.config(text="Selected File: " + filepath.split('/')[-1])
        global selected_video_path
        selected_video_path = filepath
        simulate_upload_progress(filepath, root)

def simulate_upload_progress(filepath, root):
    total_steps = 100
    for i in range(total_steps + 1):
        time.sleep(0.01)  # Simulate some processing delay
        root.after(0, lambda i=i: update_progress(i, root))

def summarize_video(root):
    global is_summarizing
    if not selected_video_path:
        messagebox.showerror("Error", "No video file selected. Please upload a video file before summarizing.")
        return
    if not selected_classes:
        messagebox.showerror("Error", "No classes selected. Please select at least one class before summarizing.")
        return
    if is_summarizing:
        messagebox.showinfo("Processing", "Summarization already in progress. Please wait until it completes.")
        return
    is_summarizing = True
    progress_bar['value'] = 0  # Reset progress bar
    messagebox.showinfo("Summarization", "Starting video summarization...")
    threading.Thread(target=lambda: run_and_enable_download(selected_video_path, selected_classes, root), daemon=True).start()
def run_and_enable_download(video_path, classes, root):
    def progress_callback(current_progress):
        # This will safely update the UI from a non-main thread
        root.after(0, lambda: update_progress(current_progress, root))

    output_video, class_detected = run_video_summarization(video_path, classes, progress_callback)
    if output_video:
        root.after(0, lambda: enable_download_button(output_video, root))
    global is_summarizing
    is_summarizing = False


def update_progress(current_progress, root):
    # Ensure this function updates the progress bar according to the received progress.
    progress_bar['value'] = current_progress
    root.update_idletasks()  # Refresh GUI


def download_video(output_video):
    file_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")])
    if file_path:
        shutil.copy(output_video, file_path)
        messagebox.showinfo("Download Successful", f"Video downloaded successfully to {file_path}")


def enable_download_button(output_video, root):
    download_btn.config(state='normal', command=lambda: download_video(output_video))
    messagebox.showinfo("Summarization Complete", "Video summarization has completed. You can now download the video.")


def create_home_tab(parent):
    logo_image = Image.open("img/logo.jpg")
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(parent, image=logo_photo, bg=forest_green)
    logo_label.image = logo_photo
    logo_label.pack(pady=20)
    description = "Video Summarization helps quickly understand video content."
    description_label = tk.Label(parent, text=description, wraplength=500, justify="left", bg=forest_green, fg='white')
    description_label.pack(pady=10)