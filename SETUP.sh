#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
USER_LOCAL_BIN="$HOME/.local/bin"

sudo mkdir -p "$USER_LOCAL_BIN/LBM/"

sudo chmod +x "$SCRIPT_DIR/src/GUI.py"
sudo ln -sf "$SCRIPT_DIR/src/GUI.py" "$USER_LOCAL_BIN/LBM/GUI"

sudo chmod +x "$SCRIPT_DIR/LBM.py"
sudo ln -sf "$SCRIPT_DIR/LBM.py" /usr/local/bin/LBM

sudo apt update
sudo apt install python3-tk python3-pip

pip3 install --user pynput

echo -e "\n\n\nSetup complete. You can run the macro from the terminal using the command: LBM -main"