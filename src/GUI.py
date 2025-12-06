#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk

# Import macro functions
import main as LBM

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

    header = ["","Slots", "Delay (s)"]
    for j, h in enumerate(header):
        ttk.Label(main_frame, text=h, style="Header.TLabel").grid(row=0, column=j, padx=2, pady=4)

    slots = []
    for i in range(1, 8):
        ttk.Label(main_frame, text=f"{i}:", style="TLabel").grid(row=i, column=0, padx=1, pady=4, sticky="e")

        var = tk.BooleanVar()
        chk = ttk.Checkbutton(main_frame, variable=var, style="TCheckbutton")
        chk.grid(row=i, column=1, padx=(0,2))

        delay_entry = ttk.Entry(main_frame, width=10, font=("Segoe UI", 10), style="TEntry")
        delay_entry.grid(row=i, column=2, padx=(0,4))
        slots.append((var, delay_entry))

    button_frame = ttk.Frame(main_frame, style="TFrame")
    button_frame.grid(row=9, column=0, columnspan=5, pady=24)

    start_btn = ttk.Button(button_frame, text="Start (F1)", command=lambda: LBM.start_macro(slots, root), style="TButton")
    start_btn.grid(row=0, column=0, padx=18, pady=8)

    pause_btn = ttk.Button(button_frame, text="Pause (F2)", command=lambda: LBM.pause_macro(root), style="TButton")
    pause_btn.grid(row=0, column=1, padx=18, pady=8)

    stop_btn = ttk.Button(button_frame, text="Stop (F3)", command=lambda: LBM.stop_macro(root), style="TButton")
    stop_btn.grid(row=1, column=0, padx=18, pady=8)

    save_btn = ttk.Button(button_frame, text="Save (F4)", command=lambda: LBM.save_settings(slots), style="TButton")
    save_btn.grid(row=1, column=1, padx=18, pady=8)

    LBM.create_INI(slots)
    LBM.load_settings(slots)

    LBM.setup_hotkeys(slots, root)

    ttk.Label(main_frame, text="Linux Hotbar Macro by Zarness and a bit of clanker", font=("Segoe UI", 10, "italic"), background="#181A20", foreground="#FF0055").grid(
        row=10, column=0, columnspan=5, pady=(24, 0)
    )

    root.mainloop()

# ---------------- Execute ---------------- #
if __name__ == "__main__":
    main()