# === STEP 1: IMPORT LIBRARIES ===
# We import necessary "toolboxes" (libraries) that Python needs.
# 'requests' is used to send requests over the internet (to talk to APIs).
# 'os' (Operating System) is used to read environment variables from the operating system.
# 'datetime' is used to convert the timestamp into a human-readable format.
import requests
import os
import datetime

# === STEP 2: GLOBAL SETTINGS AND CONSTANTS ===
# Here we define all fixed values and settings that the program uses.
# Keeping them at the top makes them easy to find and change in the future.

# --- Security Settings ---
# The code reads your secret API keys from environment variables.
# This is a secure method that ensures the keys are never written directly in the code.
OPENSKY_CLIENT_ID = os.environ.get("OPENSKY_CLIENT_ID")
OPENSKY_CLIENT_SECRET = os.environ.get("OPENSKY_CLIENT_SECRET")

# --- API Endpoints ---
# The fixed URLs for the different parts of the OpenSky API.
TOKEN_URL = "https://auth.opensky-network.org/auth/realms/opensky-network/protocol/openid-connect/token"
API_URL = "https://opensky-network.org/api/states/all"

# --- Request Headers ---
# A "User-Agent" tells the server which program is making the request.
# It's good practice to include a custom, unique User-Agent.
HEADERS = {'User-Agent': 'EyesUp/1.0 (Python)'}

# --- Geographic Areas ---
# A dictionary containing all our predefined search areas.
# Each choice (e.g., "1") points to another object containing a name for display
# and another dictionary with the exact coordinates for the search box (lamin, lomin, etc.).
# This structure makes it easy to add, remove, or change locations.
LOCATIONS = {
    "1": {"name": "Greater Gothenburg", "coords": {"lamin": 57.55, "lomin": 11.70, "lamax": 57.85, "lomax": 12.35}},
    "2": {"name": "Västra Götaland County", "coords": {"lamin": 57.2, "lomin": 10.8, "lamax": 59.8, "lomax": 14.5}},
    "3": {"name": "Stockholm Area", "coords": {"lamin": 59.10, "lomin": 17.70, "lamax": 59.70, "lomax": 18.80}}
}

# === STEP 3: HELPER FUNCTIONS ===
# Smaller, specialized functions that perform specific tasks.

def degrees_to_cardinal(d):
    """Helper function to convert degrees (0-360) to a cardinal compass direction (N, NE, E etc.)."""
    dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    ix = round(d / (360. / len(dirs)))
    return dirs[ix % len(dirs)]

def get_opensky_token():
    """
    Authenticates against the OpenSky API with Client ID and Secret to get a
    temporary Access Token. This token is then used to make the actual API calls.
    This is part of the OAuth2 security standard.
    """
    # First, a critical check: are the API keys available as environment variables?
    if not OPENSKY_CLIENT_ID or not OPENSKY_CLIENT_SECRET:
        print("[ERROR] OpenSky environment variables are not set.")
        print("        Run 'set OPENSKY_CLIENT_ID=...' and 'set OPENSKY_CLIENT_SECRET=...' in the terminal.")
        return None # Aborts the function if keys are missing.
    
    # 'try...except' is Python's way of handling errors. The code inside 'try' is executed,
    # and if an error occurs, the program jumps to the 'except' block instead of crashing.
    try:
        # This data structure (dictionary) specifies to OpenSky that we want to use
        # the "client_credentials" flow and sends our credentials.
        token_data = {"grant_type": "client_credentials", "client_id": OPENSKY_CLIENT_ID, "client_secret": OPENSKY_CLIENT_SECRET}
        
        # This is where the actual request to the OpenSky token URL is made.
        # 'requests.post' is used to send data.
        # 'timeout=10' means we will wait a maximum of 10 seconds for a response.
        response = requests.post(TOKEN_URL, headers=HEADERS, data=token_data, timeout=10)
        
        # This line checks if the response from the server was an error (e.g., 401 Unauthorized).
        # If it was an error, an exception is "raised" and the program jumps to the 'except' block.
        response.raise_for_status()
        
        # If everything went well, we convert the text response (which is in JSON format)
        # and extract our valuable "access_token".
        access_token = response.json().get("access_token")
        print("[SUCCESS] Access Token retrieved successfully.")
        return access_token # Returns the retrieved token.

    except Exception as e:
        # If any error occurred during the 'try' block, it's caught here.
        print(f"[ERROR] Failed to retrieve OpenSky Token: {e}")
        return None # Returns None to indicate failure.

def find_airplanes(opensky_token, location_info):
    """
    The main function for searching for airplanes. It receives a valid token
    and information about which location to search.
    """
    # We unpack the information from the chosen location for easier access.
    location_name = location_info["name"]
    params = location_info["coords"]

    print(f"\n[INFO] Searching for aircraft over {location_name}...")
    print("-" * (len(location_name) + 35))

    try:
        # To make an authorized request, we need to send our token.
        # The standard is to send it in an "Authorization" header with the text "Bearer " followed by the token.
        api_headers = HEADERS.copy() # We copy our standard headers
        api_headers['Authorization'] = f"Bearer {opensky_token}"
        
        # Now we make the actual request to get the aircraft data.
        # 'requests.get' is used to retrieve data.
        # 'params=params' adds our coordinates to the URL.
        response = requests.get(API_URL, headers=api_headers, params=params, timeout=10)
        response.raise_for_status() # Checks if the request failed.
        
        # We convert the JSON response and get the list of aircraft.
        plane_list = response.json().get('states')

        # If the list is empty or doesn't exist, we notify the user.
        if not plane_list:
            print("No aircraft found in your area at this time.")
            return # Exits the function.

        print(f"[INFO] Found {len(plane_list)} aircraft:\n")

        # We loop through each aircraft in the list.
        for plane_vector in plane_list:
            # Each 'plane_vector' is a list of data. We extract the data we want
            # based on its fixed position (index) in the list.
            callsign = plane_vector[1].strip() if plane_vector[1] else "Unknown"
            origin_country = plane_vector[2]
            time_position_unix = plane_vector[3]
            baro_altitude_m = plane_vector[7]
            on_ground = plane_vector[8]
            velocity_ms = plane_vector[9]
            track_degrees = plane_vector[10]
            vertical_rate_ms = plane_vector[11]
            geo_altitude_m = plane_vector[13]

            # We check if the data exists before using it to avoid errors.
            # If data exists, we format it nicely. Otherwise, we show "Unknown".
            
            # Format status based on on_ground and vertical_rate
            if on_ground:
                status_text = "On the ground"
            elif vertical_rate_ms is None:
                status_text = "In the air (level)"
            elif vertical_rate_ms > 0.3:
                status_text = f"Climbing ({vertical_rate_ms:.1f} m/s)"
            elif vertical_rate_ms < -0.3:
                status_text = f"Descending ({abs(vertical_rate_ms):.1f} m/s)"
            else:
                status_text = "In the air (level)"
            
            # Format other data points
            altitude_text = f"{int(baro_altitude_m)} m" if baro_altitude_m is not None else "Unknown"
            geo_altitude_text = f"{int(geo_altitude_m)} m" if geo_altitude_m is not None else "Unknown"
            velocity_text = f"{int(velocity_ms * 3.6)} km/h" if velocity_ms is not None else "Unknown"
            track_text = f"{int(track_degrees)}° ({degrees_to_cardinal(track_degrees)})" if track_degrees is not None else "Unknown"
            timestamp_text = datetime.datetime.fromtimestamp(time_position_unix).strftime('%Y-%m-%d %H:%M:%S') if time_position_unix else "Unknown"


            # Finally, we print all the formatted information for the user.
            print(f"Callsign: {callsign}")
            print(f"   - Origin Country: {origin_country}")
            print(f"   - Status:         {status_text}")
            print(f"   - Baro Altitude:  {altitude_text}")
            print(f"   - Geo Altitude:   {geo_altitude_text}")
            print(f"   - Velocity:       {velocity_text}")
            print(f"   - Track:          {track_text}")
            print(f"   - Last Update:    {timestamp_text}\n")

    except Exception as e:
        print(f"[ERROR] An error occurred while calling the OpenSky API: {e}")

# === STEP 4: MAIN PROGRAM ===
# This is the main logic that runs when you start the script.
def main():
    """
    The main function that controls the program flow: displays the menu,
    receives user input, and calls the other functions in the correct order.
    """
    print("Select a search area:")
    # Loops through our LOCATIONS dictionary and prints each selectable option.
    for key, value in LOCATIONS.items():
        print(f"  {key}: {value['name']}")
    
    # Asks the user to enter a number.
    choice = input(f"Enter your choice (1-{len(LOCATIONS)}): ")

    # Checks if the entered number exists as a key in our LOCATIONS dictionary.
    if choice in LOCATIONS:
        # If the choice is valid, get the information for the selected location.
        selected_location = LOCATIONS[choice]
        # Try to get a token from OpenSky.
        token = get_opensky_token()
        # If we received a token, proceed with searching for aircraft.
        if token:
            find_airplanes(token, selected_location)
    else:
        # If the choice was invalid, notify the user.
        print(f"Invalid choice. Please restart the script and select a number between 1 and {len(LOCATIONS)}.")

# === STEP 5: ENTRY POINT ===
# This special 'if' statement is standard in Python. It ensures that the 'main()' function
# is only executed when you run the file directly (e.g., with 'python EyesUp.py'),
# and not if this file were to be imported as a library into another script.
if __name__ == "__main__":
    main()
