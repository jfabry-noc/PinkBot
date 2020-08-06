#!/usr/bin/env python3
import json
import random
import sys
from pathlib import Path
from twython import Twython

# Function to verify a file exists.
def check_file(file_path):
    file_object = Path(file_path)
    if not file_object.is_file():
        # Later log this and maybe recover by running the other script.
        print("File at " + file_path + " is missing! Quitting...")
        sys.exit()

# Instantiate some variables.
color_file_path = "./pinks.json"
config_file_path = "./configuration.json"

# Verify the files.
check_file(color_file_path)
check_file(config_file_path)

# Create a seed and the map for the colors and config.
result = {}
config = {}
random.seed()

# Read the file.
with open(color_file_path) as json_file:
    color_data = json.load(json_file)
    index = random.randint(0, len(color_data) - 1)
    result = color_data[index]

if not len(result) > 0:
    print("We didn't get a color! Quitting...")
    sys.exit()

# Import the config file.
with open(config_file_path) as config_file:
    config = json.load(config_file)

# Create the Twython instance.
twitter_client = Twython(config["app_key"], config["app_secret"], config["oauth_key"], config["oauth_secret"])

# Post the status.
website = "https://www.computerhope.com/cgi-bin/htmlcolor.pl?c=" + result["hex"][1:]
rgb_nice = result["rgb"][4:len(result["rgb"])-1]
status_message = "Today's Color: " + result["name"] + "\n\nHex: " + result["hex"] + "\nRGB: " + rgb_nice + "\n\n" + website
twitter_client.update_status(status=status_message)
