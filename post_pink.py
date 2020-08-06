#!/usr/bin/env python3
import json
import random
import sys
from pathlib import Path
from twython import Twython

# Check for the color file first.
color_file_path = "./pinks.json"
color_file = Path(color_file_path)
if not color_file.is_file():
    # Later gracefully handle this, maybe run the other script.
    print("Color file is missing! Quitting...")
    sys.exit()

# Create a seed and the map.
result = {}
random.seed()

# Read the file.
with open(color_file_path) as json_file:
    color_data = json.load(json_file)
    index = random.randint(0, len(color_data) - 1)
    result = color_data[index]

if not len(result) > 0:
    print("We didn't get a color! Quitting...")
    sys.exit()
else:
    print(result)
