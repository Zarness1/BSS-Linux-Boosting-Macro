#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
USER_LOCAL_BIN="$HOME/.local/bin"

sudo chmod +x "$SCRIPT_DIR/src/main.py"
sudo ln -sf "$SCRIPT_DIR/src/main.py" "$USER_LOCAL_BIN/main"

sudo chmod +x "$SCRIPT_DIR/LBM.py"
sudo ln -sf "$SCRIPT_DIR/LBM.py" /usr/local/bin/LBM

sudo apt update
sudo apt install python3-tk python3-pip

pip3 install --user pynput

echo -e "\n\n\nSetup complete. You can run the macro from the terminal using the command: LBM -main"