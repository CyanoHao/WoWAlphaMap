# WoW Beta Map

Temporary workaround until world map localization has been complete.

## Usage

Left click: show zone map.
Right click: back to zone list.
Windows + Down Arrow: minimize window. (system shortcut)

## Development

1. Set up a virtual environment on Unix
   ```bash
   python3 -m venv venv
   . venv/bin/activate
   pip install -r requirements.txt
   ```
   or on Windows
   ```powershell
   python3 -m venv venv
   .\venv\bin\Activate.ps1
   pip install -r requirements.txt
   ```
1. Activate virtual environment on Unix
   ```bash
   . venv/bin/activate
   ```
   or on Windows
   ```powershell
   .\venv\bin\Activate.ps1
   ```
1. Run
   ```bash
   python3 main.py
   ```
   or build an app on Unix
   ```bash
   ./build.sh
   ```
   or build an app on Windows
   ```powershell
   .\build.ps1
   ```
