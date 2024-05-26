import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import threading
import time
import shutil
from tracker import run_video_summarization  # Ensure this module is correctly implemented

forest_green = '#00897B'

# Global variables to manage state
selected_video_path = ""
selected_classes = []
is_playing = False
is_paused = False
is_stopped = False

# List of classes from the MS COCO dataset for selection
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
    selected_classes = [class_combobox.get()] if class_combobox.get() else []

def play_video(video_path):
    global is_playing, is_paused, is_stopped
    cap = cv2.VideoCapture(video_path)
    target_size = (500, 500)  # Desired display size

    while cap.isOpened() and not is_stopped:
        if is_paused:
            time.sleep(0.1)  # Check every 100 ms
            continue

        ret, frame = cap.read()
        if ret and is_playing:
            (height, width) = frame.shape[:2]
            scale = target_size[0] / width if width > height else target_size[1] / height
            dim = (int(width * scale), int(height * scale))
            frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=im)
            video_label.config(image=img)
            video_label.image = img
            video_label.update()
        elif not ret:
            break

    cap.release()
    reset_video_controls()

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

def on_video_label_click(event):
    if selected_video_path:
        play_video_handler()
def update_progress(progress):
    progress_bar['value'] = progress
    root.update_idletasks()
def simulate_upload_progress(filepath):
    for _ in range(101):
        time.sleep(0.01)  # Simulate time taken to "upload"
        progress_bar['value'] += 1
        root.update_idletasks()
    video_title_label.config(text="Selected File: " + filepath.split('/')[-1])
    global selected_video_path
    selected_video_path = filepath

def upload_video():
    allowed_formats = [("MP4 files", "*.mp4"), ("AVI files", "*.avi")]
    filepath = filedialog.askopenfilename(title="Select file", filetypes=allowed_formats)
    if not filepath:
        messagebox.showinfo("Error", "No file selected")
        return
    if not filepath.lower().endswith(tuple([ext.split("*")[-1] for _, ext in allowed_formats])):
        messagebox.showerror("Error", "File format not supported. Please select a valid video file.")
        return

    video_label.config(image='')  # Clear the existing image
    video_label.image = None
    progress_bar['value'] = 0
    global selected_video_path
    selected_video_path = filepath
    download_btn.config(state='disabled')  # Disable download button after new upload
    threading.Thread(target=simulate_upload_progress, args=(filepath,), daemon=True).start()
is_summarizing = False

def summarize_video():
    global is_summarizing
    if not selected_video_path:
        messagebox.showerror("Error", "No file selected. Please select a file first.")
        return
    if not selected_classes:
        messagebox.showerror("Error", "No classes selected. Please select at least one class before summarizing.")
        return
    if is_summarizing:
        messagebox.showinfo("Processing", "Summarization is already in progress. Please wait until it completes.")
        return
    
    is_summarizing = True  # Set the flag to True as summarization starts
    messagebox.showinfo("Summarization", "Starting video summarization...")
    threading.Thread(target=lambda: run_and_enable_download(selected_video_path, selected_classes), daemon=True).start()

def run_and_enable_download(video_path, classes):
    def update_progress(progress):
        progress_bar['value'] = progress
        root.update_idletasks()

    output_video, class_detected = run_video_summarization(video_path, classes, update_progress)
    def enable_download_button():
        global is_summarizing
        download_btn.config(state='normal', command=lambda: download_video(output_video))
        
        # Always show the completion message, regardless of whether any classes were detected
        messagebox.showinfo("Summarization Complete", "Video summarization has completed successfully. You can now download the video.")
        
        is_summarizing = False  # Reset the flag to False as summarization ends

    root.after(0, enable_download_button)



def download_video(video_path):
    file_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
    if file_path:
        shutil.copy(video_path, file_path)
        messagebox.showinfo("Download", "Video downloaded successfully to " + file_path)

def create_home_tab(parent):
    logo_image = Image.open("img/logo.jpg")
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(parent, image=logo_photo, bg=forest_green)
    logo_label.image = logo_photo
    logo_label.pack(pady=20)
    description = "Video Summarization application helps users to quickly understand the content of videos."
    description_label = tk.Label(parent, text=description, wraplength=500, justify="left", bg=forest_green, fg='white')
    description_label.pack(pady=10)

root = tk.Tk()
root.title("Video Summarization App")
root.configure(bg=forest_green)
root.geometry("800x600")

notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

home_frame = tk.Frame(notebook, bg=forest_green)
notebook.add(home_frame, text='Home')
create_home_tab(home_frame)

video_summ_frame = tk.Frame(notebook, bg=forest_green)
notebook.add(video_summ_frame, text='Video Summarization')

sidebar = tk.Frame(video_summ_frame, bg=forest_green, relief='sunken', borderwidth=2)
sidebar.pack(fill='y', side='left', anchor='nw', padx=(10, 0), pady=10)

video_input_btn = tk.Button(sidebar, text="Upload Video", command=upload_video)
video_input_btn.pack(pady=(0, 10), fill='x')

progress_bar = ttk.Progressbar(sidebar, orient='horizontal', mode='determinate', length=180)
progress_bar.pack(pady=(10, 20))

class_label = tk.Label(sidebar, text="Select Class", bg=forest_green, fg='white')
class_label.pack(pady=(10, 0), fill='x')
class_combobox = ttk.Combobox(sidebar, values=coco_classes, state="readonly")
class_combobox.pack(pady=(0, 10), fill='x')
class_combobox.bind("<<ComboboxSelected>>", on_class_selection)

summarize_video_btn = tk.Button(sidebar, text="Summarize Video", command=summarize_video)
summarize_video_btn.pack(pady=(10, 20), fill='x')

download_btn = tk.Button(sidebar, text="Download Summarized Video", state='disabled')
download_btn.pack(pady=(0, 10), fill='x')

right_area = tk.Frame(video_summ_frame, bg='lightgray')
right_area.pack(fill='both', expand=True, side='right', padx=(10, 10), pady=10)

video_title_label = tk.Label(right_area, text="Selected File", bg='lightgray')
video_title_label.pack(pady=10)

video_label = tk.Label(right_area, width=500, height=500)
video_label.pack()
video_label.bind("<Button-1>", on_video_label_click)

play_btn = tk.Button(sidebar, text="Play", command=play_video_handler)
play_btn.pack(pady=(0, 5), fill='x')

pause_btn = tk.Button(sidebar, text="Pause", command=pause_video)
pause_btn.pack(pady=(0, 5), fill='x')

stop_btn = tk.Button(sidebar, text="Stop", command=stop_video)
stop_btn.pack(pady=(0, 10), fill='x')

root.mainloop()
