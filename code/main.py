import tkinter as tk
from tkinter import ttk
from code import utils   # Import the utilities file 

def main():
    root = tk.Tk()
    root.title("Video Summarization App")
    root.configure(bg=utils.forest_green)
    root.geometry("800x600")

    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)

    home_frame = tk.Frame(notebook, bg=utils.forest_green)
    notebook.add(home_frame, text='Home')
    utils.create_home_tab(home_frame)

    video_summ_frame = tk.Frame(notebook, bg=utils.forest_green)
    notebook.add(video_summ_frame, text='Video Summarization')

    sidebar = tk.Frame(video_summ_frame, bg=utils.forest_green, relief='sunken', borderwidth=2)
    sidebar.pack(fill='y', side='left', anchor='nw', padx=(10, 0), pady=10)

    video_input_btn = tk.Button(sidebar, text="Upload Video", command=lambda: utils.upload_video(root))
    video_input_btn.pack(pady=(0, 10), fill='x')

    utils.progress_bar = ttk.Progressbar(sidebar, orient='horizontal', mode='determinate', length=180)
    utils.progress_bar.pack(pady=(10, 20))

    class_label = tk.Label(sidebar, text="Select Class", bg=utils.forest_green, fg='white')
    class_label.pack(pady=(10, 0), fill='x')
    class_combobox = ttk.Combobox(sidebar, values=utils.coco_classes, state="readonly")
    class_combobox.pack(pady=(0, 10), fill='x')
    class_combobox.bind("<<ComboboxSelected>>", utils.on_class_selection)

    summarize_video_btn = tk.Button(sidebar, text="Summarize Video", command=lambda: utils.summarize_video(root))
    summarize_video_btn.pack(pady=(10, 20), fill='x')

    utils.download_btn = tk.Button(sidebar, text="Download Summarized Video", state='disabled')
    utils.download_btn.pack(pady=(0, 10), fill='x')

    right_area = tk.Frame(video_summ_frame, bg='lightgray')
    right_area.pack(fill='both', expand=True, side='right', padx=(10, 10), pady=10)

    utils.video_title_label = tk.Label(right_area, text="Selected File", bg='lightgray')
    utils.video_title_label.pack(pady=10)

    utils.video_label = tk.Label(right_area, width=500, height=500)
    utils.video_label.pack()
    utils.video_label.bind("<Button-1>", utils.on_video_label_click)

    play_btn = tk.Button(sidebar, text="Play", command=utils.play_video_handler)
    play_btn.pack(pady=(0, 5), fill='x')

    pause_btn = tk.Button(sidebar, text="Pause", command=utils.pause_video)
    pause_btn.pack(pady=(0, 5), fill='x')

    stop_btn = tk.Button(sidebar, text="Stop", command=utils.stop_video)
    stop_btn.pack(pady=(0, 10), fill='x')

    root.mainloop()

if __name__ == "__main__":
    main()
