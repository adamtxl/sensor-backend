import requests
import random
import time

URL = "http://127.0.0.1:8000/data"
HEADERS = {
    "Authorization": "Bearer tk421secret",
    "Content-Type": "application/json"
}

# Generate a random sensor payload
def generate_fake_sensor_data(sensor_id_suffix):
    return {
        "sensor_id": f"TestSensor_{sensor_id_suffix}",
        "type": "temperature",
        "value": round(random.uniform(20.0, 30.0), 2),
        "timestamp": "2025-05-07T17:05:38.469082+00:00",
        "rssi": random.randint(-80, -30),
        "snr": round(random.uniform(5.0, 15.0), 2),
        "latitude": round(random.uniform(-90.0, 90.0), 6),
        "longitude": round(random.uniform(-180.0, 180.0), 6),
        "altitude": random.randint(0, 1000)
    }

def hammer_backend(num_requests=10000, delay_between_requests=0.001):
    for i in range(num_requests):
        payload = generate_fake_sensor_data(i)
        response = requests.post(URL, headers=HEADERS, json=payload)
        if response.status_code == 200:
            print(f"✅ {i}: Successfully POSTed sensor data.")
        else:
            print(f"❌ {i}: Failed with status code {response.status_code}.")
        time.sleep(delay_between_requests)  # Small delay to avoid overload (adjust as needed)

if __name__ == "__main__":
    hammer_backend(num_requests=500, delay_between_requests=0.01)
