import requests
import json
import time

# Configuration for the AOS Broker Server
BROKER_IP = '127.0.0.1' # Use localhost since the broker is running on the same PC
BROKER_PORT = 8000
SERVER_URL = f'http://{BROKER_IP}:{BROKER_PORT}'

# Dummy Waypoint Data Structure for Drone 1
# This structure closely matches what your AOS Broker file expects (JSON with drone keys)
DRONE_MISSION_DATA = {
    "drone1": {
        "mission_waypoints": [
            {
                "latitude": 34.000000, 
                "longitude": -118.000000, 
                "altitude": 50, 
                "heading": 0,
                "speed": 5,
                "camera": 90, 
                "length_of_stay": 5, 
                "gimbal_pitch": 0, 
                "gimbal_yaw": 0
            },
            {
                "latitude": 34.000050, 
                "longitude": -118.000050, 
                "altitude": 80, 
                "heading": 45,
                "speed": 8,
                "camera": 90, 
                "length_of_stay": 0, 
                "gimbal_pitch": -45, 
                "gimbal_yaw": 0
            },
            {
                "latitude": 34.001000, 
                "longitude": -118.000000, 
                "altitude": 50, 
                "heading": 0,
                "speed": 5,
                "camera": 90, 
                "length_of_stay": 0, 
                "gimbal_pitch": 0, 
                "gimbal_yaw": 0
            }
        ]
    }
    # You can add "drone2", "drone3", etc. here if you want to test multiple drones
}

def send_waypoint_data():
    """Sends the dummy waypoint mission data as a JSON payload via HTTP POST."""
    
    headers = {'Content-Type': 'application/json'}
    json_data = json.dumps(DRONE_MISSION_DATA)

    print(f"Attempting to send waypoint data to: {SERVER_URL}")
    print(f"Data size: {len(json_data)} bytes")

    try:
        # The requests.post function sends the data as an HTTP POST request
        response = requests.post(
            SERVER_URL, 
            data=json_data, 
            headers=headers,
            timeout=5 # Set a timeout for the request
        )

        if response.status_code == 200:
            print("\n✅ Success: Data sent successfully.")
            print("Broker responded with status 200 (OK).")
            # You should now see 'Received waypoint data for drones: dict_keys(['drone1'])' 
            # or similar output in your AOS Broker terminal.
            
        else:
            print(f"\n❌ Error: Failed to send data. Server responded with status code: {response.status_code}")
            print("Check if AOS Broker is running and its server thread is active.")

    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Connection refused.")
        print(f"Ensure the AOS Broker script is running and its waypoint server is accessible at {SERVER_URL}.")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    send_waypoint_data()