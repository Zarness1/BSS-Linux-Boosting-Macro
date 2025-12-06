#!/usr/bin/env python3

# ---------------- Imports ---------------- #
import tkinter as tk
from tkinter import Toplevel, Label, Button
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

CONFIG_DIR = os.path.join(SCRIPT_DIR, "config")
os.makedirs(CONFIG_DIR, exist_ok=True)

CONFIG_FILE = os.path.join(CONFIG_DIR, "main_config.ini")

LOG_DIR = os.path.join(SCRIPT_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "crash.log")

# ---------------- Crash Logs ---------------- #
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

        if SF_S == 1:
            setting_save_popup("Settings saved", f"Settings config saved at:\n{CONFIG_FILE}")
        else:
            setting_save_popup("Settings file created", f"Settings config created at:\n{CONFIG_FILE}")

def create_INI(slots):
    global SF_S
    SF_S = 1
    if not os.path.exists(CONFIG_FILE):
        SF_S = 0
        save_settings(slots)
        SF_S = 1

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
