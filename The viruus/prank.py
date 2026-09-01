import tkinter as tk
import pygame
import cv2
from PIL import Image, ImageTk
import random
import sys, os   # <-- add this

# Helper to find files whether running as .py or .exe
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

pygame.mixer.init()
pygame.mixer.music.load(resource_path("alarm.mp3"))   # <-- fixed

def start_prank():
    pygame.mixer.music.play(-1)
    flash_text()
    root.after(2000, play_video)

def flash_text():
    current_color = warning_label.cget("fg")
    new_color = "white" if current_color == "red" else "red"
    warning_label.config(fg=new_color)
    root.after(500, flash_text)

def play_video():
    warning_label.place_forget()
    cap = cv2.VideoCapture(resource_path("winerror.mp4"))  # <-- fixed
    show_frame(cap)

def show_frame(cap):
    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (screen_w, screen_h))
        img = ImageTk.PhotoImage(Image.fromarray(frame))
        video_label.config(image=img)
        video_label.image = img
        root.after(30, lambda: show_frame(cap))
    else:
        cap.release()
        freeze_last_frame()

def freeze_last_frame():
    pygame.mixer.music.stop()
    warning_label.config(
        text="💀 SYSTEM CRASH 💀\nBlue Screen of Death!",
        font=("Arial", 32, "bold"), fg="blue", bg="black"
    )
    warning_label.place(relx=0.5, rely=0.5, anchor="center")
    spawn_popup()  # start popups immediately

popup_count = 0  # global counter

def spawn_popup(auto=False):
    global popup_count
    popup_count += 1

    x = random.randint(100, screen_w - 400)
    y = random.randint(100, screen_h - 200)
    popup = tk.Toplevel(root)
    popup.title("System Error")
    popup.geometry(f"300x150+{x}+{y}")
    popup.configure(bg="black")

    # Stage messages
    if popup_count <= 3:
        text = "⚠ Malware Detected ⚠"
        color = "red"
    elif popup_count <= 6:
        text = "Virus Injected!\nSystem Breach!"
        color = "red"
    else:
        text = "LOL you got pranked!\nclick on blue screen then\nPress ESC to exit."
        color = "green"

    msg = tk.Label(popup, text=text,
                   font=("Arial", 12, "bold"), fg=color, bg="black")
    msg.pack(expand=True)

    btn = tk.Button(popup, text="Close", command=spawn_popup,
                    bg="red", fg="white")
    btn.pack()

    popup.protocol("WM_DELETE_WINDOW", spawn_popup)

    # Auto‑spawn new popup every 3 seconds
    if not auto:
        root.after(3000, lambda: spawn_popup(auto=True))

def escape(event=None):
    pygame.mixer.music.stop()
    root.destroy()

root = tk.Tk()
root.title("Fake Virus Prank")
root.attributes("-fullscreen", True)
root.configure(bg="black")

screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()

warning_label = tk.Label(root,
    text="⚠ SYSTEM ERROR DETECTED ⚠",
    font=("Arial", 32, "bold"), fg="red", bg="black"
)
warning_label.place(relx=0.5, rely=0.2, anchor="center")

video_label = tk.Label(root, bg="black")
video_label.place(x=0, y=0)

root.bind("<Escape>", escape)

start_prank()
root.mainloop()
