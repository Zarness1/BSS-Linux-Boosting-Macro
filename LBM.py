#!/usr/bin/env python3
import os
import sys
import subprocess

# ---------------- File Paths ---------------- #
LOCAL_BIN = os.path.expanduser("~/.local/bin/LBM/")
GUI_FILE = "GUI"
GUI_PATH = os.path.join(LOCAL_BIN, GUI_FILE)

# ---------------- Functions ---------------- #
def help():
    print("""
Usage: LBM [arg]
Args:
  -h            Show this help message
  -main         Run the macro for main account
""")

def run(args):
    if not os.path.exists(GUI_PATH):
        print(f"Error: Macro GUI file not found at {GUI_PATH}")
        return
    
    subprocess.run(["python3", GUI_PATH] + args)

def main():
    if len(sys.argv) == 1:
        print("No argument provided. Use LBM -h for help.")
        return
    
    arg = sys.argv[1]

    if arg == "-h":
        help()

    elif arg == "-main":
        run(sys.argv[2:])

    else:
        print(f"Unknown argument: {arg}")
        help()

# ---------------- Execute ---------------- #
if __name__ == "__main__":
    main()
