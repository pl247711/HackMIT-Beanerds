#install this: pip install Flask requests
import requests
import time

API_BASE_URL = "https://terra-api.example.com" # change this to the actual base URL for Terra's API
AUTH_ENDPOINT = "/auth/token" # replace with the actual auth endpoint if different
API_KEY = "YOUR_API_KEY" # method Terra uses for authentication
DATA_ENDPOINT = "/fitbit-data" # Replace with actual endpoint
HISTORICAL_DATA_ENDPOINT = "/fitbit-data/history"  # replace this
INTERVAL = 180 # 3 minutes in seconds


def get_access_token():
    response = requests.post(f"{API_BASE_URL}{AUTH_ENDPOINT}", data={"api_key": API_KEY})
    if response.status_code == 200:
        return response.json().get('access_token')
    return None

def pull_data_regularly():
    access_token = get_access_token() 
    if not access_token:
        print("Failed to authenticate.")
        return

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    while True:
        response = requests.get(f"{API_BASE_URL}{DATA_ENDPOINT}", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            heart_rate = data.get('heart_rate') # whatever the data is called
            physical_activity = data.get('physical_activity') # whatever
            # Do something with data, like saving it or processing it
            print(f"Heart Rate: {heart_rate}, Physical Activity: {physical_activity}")
        else:
            print(f"Failed to pull data. Status Code: {response.status_code}")
        time.sleep(INTERVAL)


def fetch_historical_data(start_date, end_date):
    access_token = get_access_token() 
    if not access_token:
        print("Failed to authenticate.")
        return

    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    params = {
        "start_date": start_date,
        "end_date": end_date
    }

    response = requests.get(f"{API_BASE_URL}{HISTORICAL_DATA_ENDPOINT}", headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        # might be a list of data points given it's historical
        for entry in data:
            heart_rate = entry.get('heart_rate')
            physical_activity = entry.get('physical_activity')

if __name__ == "__main__":
    pull_data_regularly()
