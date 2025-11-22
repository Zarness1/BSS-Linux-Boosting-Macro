#!/usr/bin/env python3

# ---------------- Imports ---------------- #
import tkinter as tk
from tkinter import ttk, Toplevel, Label, Button
import threading
import time
import configparser
import os
from pynput import keyboard
from pynput.keyboard import Controller
import faulthandler

# ---------------- Global States ---------------- #
running = False
paused = False
stop = False
keyboard_controller = Controller()

# ---------------- File Paths ---------------- #
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

CONFIG_DIR = os.path.join(SCRIPT_DIR, "configuration")
os.makedirs(CONFIG_DIR, exist_ok=True)

CONFIG_FILE = os.path.join(CONFIG_DIR, "main_macro_settings_config.ini")

LOG_DIR = os.path.join(SCRIPT_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "crash.log")

# ---------------- Logs ---------------- #
f = open(LOG_FILE, "a")
faulthandler.enable(file=f, all_threads=True)

# ---------------- Key Press ---------------- #
def send_keystroke(key):
    keyboard_controller.press(key)
    time.sleep(0.05)
    keyboard_controller.release(key)

# ---------------- Worker Threads ---------------- #
def slot_worker(slot_id, delay):
    global running, paused, stop
    while running and not stop:
        if paused:
            time.sleep(0.1)
            continue
        send_keystroke(str(slot_id))
        time.sleep(delay)

# ---------------- Macro Control ---------------- #
def start_macro(slots, root):
    global running, paused, stop
    if not running:
        running = True
        paused = False
        stop = False
        root.withdraw()

    for i, (var, delay_entry) in enumerate(slots, start=1):
        if var.get():
            try:
                delay = float(delay_entry.get())
            except ValueError:
                continue

            threading.Thread(
                target=slot_worker,
                args=(i, delay),
                daemon=True
            ).start()

def pause_macro(root):
    global paused
    paused = True
    root.deiconify()

def stop_macro(root):
    global running, paused, stop
    running = False
    paused = False
    stop = True
    root.deiconify()

# ---------------- Settings INI Handling ---------------- #
def save_settings(slots):
    config = configparser.ConfigParser()
    config["Slots"] = {}
    for i, (var, delay_entry) in enumerate(slots, start=1):
        config["Slots"][f"slot{i}_enabled"] = str(var.get())
        config["Slots"][f"slot{i}_delay"] = delay_entry.get()


    with open(CONFIG_FILE, "w") as f:
        config.write(f)

        def setting_save_popup(title, message):
            popup = Toplevel()
            popup.title(title)
            popup.resizable(False, False)

            Label(popup, text=message, wraplength=520, justify="left", font=("Segoe UI", 11, "bold")).pack(pady=20, padx=20)
            Button(popup, text="OK", command=popup.destroy, width=10).pack(pady=10)

            popup.grab_set()

        setting_save_popup("Settings Saved", f"Settings configuration saved at:\n{CONFIG_FILE}")

def create_default_INI(slots):
    if not os.path.exists(CONFIG_FILE):
        save_settings(slots)

def load_settings(slots):
    if not os.path.exists(CONFIG_FILE):
        return
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    if "Slots" not in config:
        return
    for i, (var, delay_entry) in enumerate(slots, start=1):
        try:
            var.set(config.getboolean("Slots", f"slot{i}_enabled", fallback=False))
            delay_entry.delete(0, tk.END)
            delay_entry.insert(0, config.get("Slots", f"slot{i}_delay", fallback=""))
        except Exception:
            continue


# ---------------- Hotkeys ---------------- #
def setup_hotkeys(slots, root):
    def on_press(key):
        try:
            if key == keyboard.Key.f1:
                start_macro(slots, root)
            elif key == keyboard.Key.f2:
                pause_macro(root)
            elif key == keyboard.Key.f3:
                stop_macro(root)
            elif key == keyboard.Key.f4:
                save_settings(slots)
        except Exception as e:
            print("Error:", e)

    listener = keyboard.Listener(on_press=on_press)
    listener.daemon = True
    listener.start()

# ---------------- GUI ---------------- #
def main():
    root = tk.Tk()
    root.title("Linux BSS Boosting Macro")
    root.geometry("360x480")
    root.resizable(False, False)

    style = ttk.Style()
    root.tk_setPalette(background="#181A20", foreground="#F0F0F0", activeBackground="#23262F", activeForeground="#F0F0F0")
    style.theme_use("clam")
    style.configure("TFrame", background="#181A20")
    style.configure("TLabel", background="#181A20", foreground="#F0F0F0", font=("Segoe UI", 11))
    style.configure("Header.TLabel", background="#181A20", foreground="#FF0055", font=("Segoe UI", 12, "bold"))
    style.configure("TCheckbutton", background="#181A20", foreground="#F0F0F0", font=("Segoe UI", 11))
    style.configure("TEntry", fieldbackground="#23262F", foreground="#F0F0F0", font=("Segoe UI", 11))
    style.configure("TButton", background="#23262F", foreground="#FF0055", font=("Segoe UI", 11, "bold"), borderwidth=0, focusthickness=3, focuscolor="#FF0055")
    style.map("TButton",
        background=[("active", "#FF0055"), ("pressed", "#23262F")],
        foreground=[("active", "#181A20"), ("pressed", "#FF0055")]
    )

    main_frame = ttk.Frame(root, padding=18, style="TFrame")
    main_frame.pack(fill=tk.BOTH, expand=True)

    header = ["", "Slots", "Delay (s)"]
    for j, h in enumerate(header):
        ttk.Label(main_frame, text=h, style="Header.TLabel").grid(row=0, column=j, padx=2, pady=4)

    slots = []
    for i in range(1, 8):
        ttk.Label(main_frame, text=f"Slot {i}:", style="TLabel").grid(row=i, column=0, padx=1, pady=4, sticky="e")

        var = tk.BooleanVar()
        chk = ttk.Checkbutton(main_frame, variable=var, style="TCheckbutton")
        chk.grid(row=i, column=1, padx=(0,2))

        delay_entry = ttk.Entry(main_frame, width=10, font=("Segoe UI", 10), style="TEntry")
        delay_entry.grid(row=i, column=2, padx=(0,4))
        slots.append((var, delay_entry))

    button_frame = ttk.Frame(main_frame, style="TFrame")
    button_frame.grid(row=9, column=0, columnspan=5, pady=24)

    start_btn = ttk.Button(button_frame, text="Start (F1)", command=lambda: start_macro(slots, root), style="TButton")
    start_btn.grid(row=0, column=0, padx=18, pady=8)

    pause_btn = ttk.Button(button_frame, text="Pause (F2)", command=lambda: pause_macro(root), style="TButton")
    pause_btn.grid(row=0, column=1, padx=18, pady=8)

    stop_btn = ttk.Button(button_frame, text="Stop (F3)", command=lambda: stop_macro(root), style="TButton")
    stop_btn.grid(row=1, column=0, padx=18, pady=8)

    save_btn = ttk.Button(button_frame, text="Save (F4)", command=lambda: save_settings(slots), style="TButton")
    save_btn.grid(row=1, column=1, padx=18, pady=8)

    create_default_INI(slots)
    load_settings(slots)

    setup_hotkeys(slots, root)

    ttk.Label(main_frame, text="Linux Hotbar Macro by Zarness and a bit of clanker", font=("Segoe UI", 10, "italic"), background="#181A20", foreground="#FF0055").grid(
        row=10, column=0, columnspan=5, pady=(24, 0)
    )

    root.mainloop()

# ---------------- Launch ---------------- #
if __name__ == "__main__":
    main()