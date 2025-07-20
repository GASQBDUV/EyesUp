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
   ```

3. **Set Environment Variables:**
   This is the most critical step. You must set your API credentials as environment variables in the **same terminal session** where you will run the script.

   * **On Windows (Command Prompt):**
     ```cmd
     set OPENSKY_CLIENT_ID=your_client_id_here
     set OPENSKY_CLIENT_SECRET=your_client_secret_here
     ```

   * **On macOS or Linux (Terminal):**
     ```bash
     export OPENSKY_CLIENT_ID="your_client_id_here"
     export OPENSKY_CLIENT_SECRET="your_client_secret_here"
     ```
   > **Note:** Replace `your_client_id_here` and `your_client_secret_here` with the actual credentials you obtained from OpenSky.

4. **Run the Script:**
   Navigate to the script's directory in your terminal and run it using Python.
   ```bash
   python EyesUp.py
   ```
   (You may need to use `python3` on macOS/Linux).

5. **Follow On-Screen Instructions:**
   The script will prompt you to select a geographical area. Enter the corresponding number and press Enter.

## Example Output

```
[SUCCESS] Access Token retrieved successfully.

[INFO] Searching for aircraft over Stockholm Area...
------------------------------------------------------------
[INFO] Found 12 aircraft:

Callsign: RYR78P
   - Origin Country: Ireland
   - Status:         Descending (7.9 m/s)
   - Baro Altitude:  3421 m
   - Geo Altitude:   3581 m
   - Velocity:       588 km/h
   - Track:          166° (SSE)
   - Last Update:    2025-07-20 14:30:00

Callsign: SAS405
   - Origin Country: Sweden
   - Status:         Climbing (11.2 m/s)
   - Baro Altitude:  6780 m
   - Geo Altitude:   6919 m
   - Velocity:       750 km/h
   - Track:          271° (W)
   - Last Update:    2025-07-20 14:30:01
```

## Data Source

This project relies entirely on the fantastic, free, and open data provided by the [**OpenSky Network**](https://opensky-network.org). Please consider supporting their project or contributing data if you have a receiver.
