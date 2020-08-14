#!/usr/bin/env python3
import json
import logging
import os
import random
import requests
import sys
from bs4 import BeautifulSoup
from pathlib import Path
from twython import Twython

# Function to verify a file exists.
def check_file(file_path):
    file_object = Path(file_path)
    if not file_object.is_file():
        # Check if it's the color file.
        logging.error("No color file found! Running get_pinks.py...")
        if file_path == "./pinks.json":
            exec(open("get_pinks.py").read())
        else:
            logging.error("Couldn't find get_pinks.py! Quitting...")
            sys.exit()

# Function to back up the log file if it's too large.
def backup_log_file():
    if os.path.isfile("./log.txt"):
        # Get the size.
        log_size = os.path.getsize("./log.txt")
        # Act if it's bigger than 10 MB.
        if log_size >= 10000000:
            # See if a backup exists.
            if os.path.isfile("./log.BKP"):
                # Nuke it.
                try:
                    os.remove("./log.BKP")
                except:
                    logging.error("Backup log found but couldn't be removed. Make sure it isn't locked by an application.")
                    logging.error("Quitting...")
                    sys.exit(4)

                # Rename the existing file.
                try:
                    os.rename("./log.txt", "./log.BKP")
                except:
                    logging.error("Couldn't rename usage.log to usage.BKP. Make sure the log isn't locked by an application.")
                    logging.error("Quitting...")
                    sys.exit(5)

# Main code here.
# Set the directory for the cron job
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# Set the logging.
logging.basicConfig(
    filename = "./log.txt",
    level = logging.INFO,
    format = "%(asctime)s:%(levelname)s:%(message)s"
        )

# Check if we need to backup the log file.
backup_log_file()

# Log the start of the script.
logging.info("###########################################################################")
logging.info("Starting the script...")

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
logging.info("Getting today's color.")
with open(color_file_path) as json_file:
    color_data = json.load(json_file)
    index = random.randint(0, len(color_data) - 1)
    result = color_data[index]

# Make sure we got something.
if not len(result) > 0:
    logging.error("We didn't get a color! Quitting...")
    sys.exit()

# Import the config file.
logging.info("Loading the config file.")
with open(config_file_path) as config_file:
    config = json.load(config_file)

# Create the Twython instance.
logging.info("Creating the Twitter client.")
twitter_client = Twython(config["app_key"], config["app_secret"], config["oauth_key"], config["oauth_secret"])

# Post the status.
logging.info("Making the Twitter post.")
website = "https://www.computerhope.com/cgi-bin/htmlcolor.pl?c=" + result["hex"][1:]
rgb_nice = result["rgb"][4:len(result["rgb"])-1]
status_message = "Today's Color: " + result["name"] + "\n\nHex: " + result["hex"] + "\nRGB: " + rgb_nice + "\n\n" + website
try:
    twitter_client.update_status(status=status_message)
except:
    error = sys.exc_info()[0]
    logging.error("Error posting: " + str(error))

# Log the end.
logging.info("Gracefully completed the script.")
