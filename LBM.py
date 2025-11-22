#!/usr/bin/env python3
import os
import sys
import subprocess

LOCAL_BIN = os.path.expanduser("~/.local/bin/")
MAIN_FILE = "main"
TARGET_PATH = os.path.join(LOCAL_BIN, MAIN_FILE)

def help():
    print("""
Usage: LBM [flag]
Flags:
  -h            Show this help message
  -main         Run the macro for main account
""")

def run_main_macro(extra_args):
    if not os.path.exists(TARGET_PATH):
        print(f"Error: Macro file not found at {TARGET_PATH}")
        return
    subprocess.run(["python3", TARGET_PATH] + extra_args)

def main():
    if len(sys.argv) == 1:
        print("No flag provided. Use LBM -h for help.")
        return
    
    flag = sys.argv[1]

    if flag == "-h":
        help()

    elif flag == "-main":
        run_main_macro(sys.argv[2:])

    else:
        print(f"Unknown flag: {flag}")
        help()

if __name__ == "__main__":
    main()
