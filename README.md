# Window-Focus-OSC

A simple tool for managing and controlling program windows via **OSC**.

## Features
- **Set OSC Port:** Dynamically change OSC port via the GUI.
- **OSC Path:** `/program [value]` where `value` corresponds to the program order.
- **Log Programs:** Automatically log visible programs to `log.txt`.
- **Custom Order:** Copy program names from `log.txt` to `list.txt` to define custom control order.
- **Refresh Program List:** Quickly update the visible programs.

## How It Works
1. **List Programs:** Visible windows are listed in `log.txt`.
2. **Customize Order:** Copy program names to `list.txt`.
3. **Control Windows:** Send OSC commands like `/program 1` to focus on the first program in `list.txt`.

## Usage
1. Run the program:  
   ```bash
   python Window-Focus-OSCv5.py
