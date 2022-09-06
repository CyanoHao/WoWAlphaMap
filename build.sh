#!/bin/sh
pyinstaller --onefile --windowed --strip --add-data gallery:gallery --name WoWBetaMap main.py
