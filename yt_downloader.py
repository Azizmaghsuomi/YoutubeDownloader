import os
import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import ttkbootstrap as ttkb  # برای رابط گرافیکی مدرن

COOKIES_PATH = r"C:\Users\myhp2\Downloads\www.youtube.com_cookies"

def fetch_formats():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter the video link!")
        return

    try:
        # نمایش "Fetching..." کنار دکمه دانلود
        fetching_label.config(text="Fetching...")
        app.update()  # بروزرسانی رابط کاربری

        result = subprocess.run(
            ["yt-dlp", "--cookies", COOKIES_PATH, "-F", url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # پاک کردن "Fetching..." بعد از بارگذاری
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

def download_video():
    try:
        selected_video = video_listbox.get(video_listbox.curselection())
        if not selected_video:
            messagebox.showerror("Error", "Please select a video format!")
            return

        video_format = selected_video.split()[0]
        audio_format = "140"
        url = url_entry.get()
        output_path = output_dir.get()

        if not output_path:
            output_path = os.getcwd()

        cmd = [
            "yt-dlp",
            "--cookies", COOKIES_PATH,
            "-f", f"{video_format}+{audio_format}",
            "-o", f"{output_path}/%(title)s.%(ext)s",
            url
        ]

        log_box.delete(1.0, tk.END)  # پاک کردن متن قبلی

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        for line in process.stdout:
            if "%" in line:
                # پاک کردن خط قبلی و نمایش خط جدید
                log_box.delete(1.0, tk.END)
                
                # جداسازی درصد برای رنگ‌آمیزی
                start_idx = line.find("[download]") + len("[download] ")
                end_idx = line.find("%") + 1
                
                log_box.insert(tk.END, line[:start_idx], "green_text")  # متن عادی سبز
                log_box.insert(tk.END, line[start_idx:end_idx], "blue_text")  # درصد آبی
                log_box.insert(tk.END, line[end_idx:], "green_text")  # باقی‌مانده سبز
            else:
                log_box.delete(1.0, tk.END)
                log_box.insert(tk.END, line.strip(), "green_text")
                
            app.update_idletasks()  # بروزرسانی رابط کاربری

        process.wait()

        if process.returncode == 0:
            log_box.delete(1.0, tk.END)
            log_box.insert(tk.END, "Download completed successfully!", "green_text")
            
            # پاک کردن همه ورودی‌ها بعد از دانلود ویدیو
            video_listbox.delete(0, tk.END)
            log_box.delete(1.0, tk.END)

            messagebox.showinfo("Success", "download successfully!")
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

app = ttkb.Window(themename="darkly")
app.title("AzizDownloader")

frame = ttk.Frame(app)
frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

ttk.Label(frame, text="AzizDownloader", font=("Segoe UI", 24, "bold")).grid(row=0, column=0, columnspan=3, pady=10)

ttk.Label(frame, text="Video URL:", font=("Segoe UI", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
url_entry = ttk.Entry(frame, width=40)
url_entry.grid(row=1, column=1, padx=10, pady=10)
ttk.Button(frame, text="Fetch Formats", command=fetch_formats).grid(row=1, column=2, padx=10, pady=10)

ttk.Label(frame, text="Video Formats:", font=("Segoe UI", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="w")
video_listbox = tk.Listbox(frame, width=60, height=8, selectmode=tk.SINGLE, exportselection=False, font=("Segoe UI", 12), bd=2, relief="solid")
video_listbox.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

ttk.Label(frame, text="Save To:", font=("Segoe UI", 12)).grid(row=3, column=0, padx=10, pady=10, sticky="w")
output_dir = tk.StringVar()
output_entry = ttk.Entry(frame, textvariable=output_dir, width=30)
output_entry.grid(row=3, column=1, padx=10, pady=10)
ttk.Button(frame, text="Browse", command=browse_folder).grid(row=3, column=2, padx=10, pady=10)

log_box = tk.Text(frame, width=60, height=1, font=("Courier", 10), bg="black", fg="green")
log_box.tag_configure("green_text", foreground="green")  # Green for normal text
log_box.tag_configure("red_text", foreground="red")  # Red for error
log_box.tag_configure("blue_text", foreground="blue")  # Blue for percentages
log_box.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

# برچسب برای نمایش "Fetching..."
fetching_label = ttk.Label(frame, text="", font=("Segoe UI", 20), foreground="orange")
fetching_label.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

# دکمه دانلود با رنگ سبز و گوشه‌های گرد
ttk.Button(frame, text="Download", command=download_video, bootstyle="success", width=40).grid(row=6, column=0, columnspan=3, pady=20)

app.mainloop()
