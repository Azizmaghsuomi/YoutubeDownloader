import os
import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import ttkbootstrap as ttkb  # برای رابط گرافیکی مدرن

COOKIES_PATH = r"C:\Users\myhp2\Downloads\py-downlpader\www.youtube.com_cookies"

# توابع مورد نیاز
def fetch_formats():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter the video link!")
        return

    try:
        fetching_label.config(text="Fetching...")
        app.update()

        result = subprocess.run(
            ["yt-dlp", "--cookies", COOKIES_PATH, "-F", url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        fetching_label.config(text="")
        
        if result.returncode != 0:
            messagebox.showerror("Error", "Failed to fetch available formats.")
            return

        output_text = result.stdout
        video_listbox.delete(0, tk.END)
        
        for line in output_text.split("\n"):
            if line.strip() and line[0].isdigit() and ("video only" in line or "audio only" in line):
                video_listbox.insert(tk.END, line.strip())
        messagebox.showinfo("Success", "Available formats loaded!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

def toggle_fetch_button():
    if subtitle_var.get():
        fetch_button.config(state=tk.DISABLED, bootstyle="secondary")
    else:
        fetch_button.config(state=tk.NORMAL, bootstyle="primary")

def download_video():
    try:
        url = url_entry.get()
        output_path = output_dir.get()
        if not output_path:
            output_path = os.getcwd()

        if subtitle_var.get():
            cmd = [
                "yt-dlp",
                "--cookies", COOKIES_PATH,
                "--write-auto-sub", "--sub-lang", "en",
                "--skip-download",
                "-o", f"{output_path}/%(title)s.%(ext)s",
                url
            ]
        else:
            selected_video = video_listbox.get(video_listbox.curselection())
            if not selected_video:
                messagebox.showerror("Error", "Please select a video format!")
                return
            video_format = selected_video.split()[0]
            audio_format = "140"
            cmd = [
                "yt-dlp",
                "--cookies", COOKIES_PATH,
                "-f", f"{video_format}+{audio_format}",
                "-o", f"{output_path}/%(title)s.%(ext)s",
                url
            ]

        log_box.delete(1.0, tk.END)

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        for line in process.stdout:
            if "%" in line:
                log_box.delete(1.0, tk.END)
                start_idx = line.find("[download]") + len("[download] ")
                end_idx = line.find("%") + 1
                
                log_box.insert(tk.END, line[:start_idx], "green_text")
                log_box.insert(tk.END, line[start_idx:end_idx], "blue_text")
                log_box.insert(tk.END, line[end_idx:], "green_text")
            else:
                log_box.delete(1.0, tk.END)
                log_box.insert(tk.END, line.strip(), "green_text")
                
            app.update_idletasks()

        process.wait()

        if process.returncode == 0:
            log_box.delete(1.0, tk.END)
            log_box.insert(tk.END, "Download completed successfully!", "green_text")
            video_listbox.delete(0, tk.END)
            log_box.delete(1.0, tk.END)

            url_entry.delete(0, tk.END)
            output_dir.set("")

            messagebox.showinfo("Success", "Download completed successfully!")
        else:
            log_box.delete(1.0, tk.END)
            log_box.insert(tk.END, "Failed to download the video.", "red_text")
    except tk.TclError:
        messagebox.showerror("Error", "Please select a valid video format.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        output_dir.set(folder)

# ساخت رابط گرافیکی
app = ttkb.Window(themename="darkly")
app.title("AzizDownloader")

frame = ttk.Frame(app)
frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

ttk.Label(frame, text="AzizDownloader", font=("Segoe UI", 24, "bold")).grid(row=0, column=0, columnspan=4, pady=10)

ttk.Label(frame, text="Video URL:", font=("Segoe UI", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
url_entry = ttk.Entry(frame, width=40)
url_entry.grid(row=1, column=1, padx=10, pady=10)

fetch_button = ttk.Button(frame, text="Fetch Formats", command=fetch_formats, bootstyle="primary")
fetch_button.grid(row=1, column=2, padx=10, pady=10)

subtitle_var = tk.BooleanVar()
subtitle_checkbox = ttk.Checkbutton(frame, text="Subtitles Only", variable=subtitle_var, command=toggle_fetch_button)
subtitle_checkbox.grid(row=1, column=3, padx=10, pady=10)

ttk.Label(frame, text="Video Formats:", font=("Segoe UI", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
video_listbox = tk.Listbox(frame, width=60, height=8, selectmode=tk.SINGLE, exportselection=False, font=("Segoe UI", 12), bd=2, relief="solid")
video_listbox.grid(row=2, column=1, columnspan=3, padx=10, pady=10)

ttk.Label(frame, text="Save To:", font=("Segoe UI", 12)).grid(row=3, column=0, padx=10, pady=10, sticky="w")
output_dir = tk.StringVar()
output_entry = ttk.Entry(frame, textvariable=output_dir, width=30)
output_entry.grid(row=3, column=1, padx=10, pady=10)
ttk.Button(frame, text="Browse", command=browse_folder).grid(row=3, column=2, padx=10, pady=10)

log_box = tk.Text(frame, width=60, height=1, font=("Courier", 10), bg="black", fg="green")
log_box.tag_configure("green_text", foreground="#0c8709")
log_box.tag_configure("red_text", foreground="red")
log_box.tag_configure("blue_text", foreground="#ffffff")
log_box.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

fetching_label = ttk.Label(frame, text="", font=("Segoe UI", 20), foreground="orange")
fetching_label.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

ttk.Button(frame, text="Download", command=download_video, bootstyle="success", width=40).grid(row=6, column=0, columnspan=4, pady=20)

app.mainloop()
