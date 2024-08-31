#!/bin/sh
pgrep -f "python3 ./main.py" | xargs kill >/dev/null 2>&1
