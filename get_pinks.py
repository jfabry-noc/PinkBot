#!/usr/bin/env python3
import json
import requests
from bs4 import BeautifulSoup

# Function to scrape the site.
def scrape_content(url):
    # Define the list that will store everything.
    rows = []

    # Set up the request to get junk from the Internet.
    page = requests.get(url)
    page_content = page.content

    # Parse the content as HTML.
    soup = BeautifulSoup(page_content, "html.parser")

    # Find the divs we care about.
    divisions = soup.find_all("div", {"class": "color-inner"})

    # Loop through each div.
    for division in divisions:
        # Get the name, hex, and RGB codes.
        color_name = division.find("span", {"class": "color-sub"}).get_text()
        color_hex = division.find("span", {"class": "color-id"}).get_text()
        color_rgb = division.find("span", {"class": "color-rgb"}).get_text()

        # Make a dictionary and append to the list.
        rows.append({"name": color_name, "hex": color_hex, "rgb": color_rgb})

    # Return the list.
    return rows
    
all_colors = scrape_content('https://html-color.codes/pink#:~:text=Pink%20Color%20Codes%3A%20colors%20shown%20are%20similar%20to,palevioletred%3A%20%23db7093%20%2F%20rgb%28219%2C112%2C147%29%20deeppink%3A%20%23ff1493%20%2F%20rgb%28255%2C20%2C147%29')

with open('pinks.json', 'w') as outfile:
    json.dump(all_colors, outfile)
