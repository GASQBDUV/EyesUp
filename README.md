# EyesUP
Quickly see what planes are above you right now.
# Eyes Up - Real-Time Flight Scanner

A simple yet powerful Python script that fetches and displays real-time flight data for a selected geographical area using the public OpenSky Network API.

This script is designed as an educational tool to demonstrate API integration, data handling, and basic command-line user interaction in Python. It's fully commented to be easily understood by beginners.

## Features

* **Real-Time Data:** Fetches live flight data with minimal delay.
* **Geographic Selection:** Choose from several predefined areas, including local, regional, and major metropolitan zones.
* **Detailed Flight Information:** Displays key data for each aircraft, including:
  * Callsign
  * Origin Country
  * Flight Status (On Ground, Climbing, Descending, Level)
  * Barometric and Geometric Altitude
  * Ground Velocity (in km/h)
  * Track (in degrees and cardinal direction)
  * Time of last position update
* **Secure API Key Handling:** Uses environment variables to securely manage API credentials, ensuring they are never hard-coded.
* **Cross-Platform:** Works on Windows, macOS, and Linux.

## Requirements

* Python 3.6 or newer
* The `requests` Python library
* An active internet connection
* API Credentials from OpenSky Network

## Setup

Before running the script, you need to get free API credentials from the OpenSky Network.

1. **Create an Account:** Go to the [OpenSky Network registration page](https://opensky-network.org/my-account/register) and create a free account.
2. **Activate API Client:** Log in to your account, navigate to your Dashboard/Account page, and find the "API Client" section. Follow the instructions to create a new API client.
3. **Get Credentials:** Once created, you will be provided with a **`Client ID`** and a **`Client Secret`**. You will need these for the next step.

## How to Run

1. **Clone or Download:**
   Download the `EyesUp.py` script to a folder on your computer.

2. **Install `requests` library:**
   Open your terminal or command prompt and run:
   ```bash
   pip install requests
