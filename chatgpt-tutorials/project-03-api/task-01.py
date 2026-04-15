import requests
from requests.exceptions import HTTPError, Timeout
import time
from datetime import datetime

""" 
    API Monitor Tool that checks the status and response time of 
    each API and alerts if any API is down or slow. 
    It runs indefinitely until interrupted by the user.   
"""
SLOW_THRESHOLD = 1.0 # SECONDS

# Function to check the status and response time of each API
def check_apis(urls):
    # Iterate through the list of URLs and make a GET request to each one
    for url in urls:
       
        try:
            # Record the start time, make the GET request, 
            # and record the end time
            start = time.time()
            response = requests.get(url, timeout=5)
            end = time.time()
            elapsed = end - start 
            response.raise_for_status()

            # Check if the response time exceeds the slow threshold and print the appropriate message   
            if elapsed >  SLOW_THRESHOLD:
                print(f"ALERT: {url} -> SLOW ({response.status_code}) - ({elapsed:.3f}s)")
            else:
                print(f"{url} -> OK {response.status_code} - {elapsed:.3f}s")
        except Timeout:
            print(f"ALERT: {url} -> TIMEOUT")
        except HTTPError as http_err:
            print(f"ALERT: {url} -> HTTP ERROR: {http_err}")
        except Exception as err:
            print(f"ALERT: {url} -> ERROR: {err}")

def main():
    urls = [
        "https://api.ipstack.com", 
        "http://colormind.io/api"
    ]
    interval = 5

    # Run the monitoring loop indefinitely until interrupted by the user
    while True:
        try:

            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Checking APIs...")
            print("-" * 50)

            check_apis(urls)

            time.sleep(interval)

        except KeyboardInterrupt:
            print("\nMonitoring stopped")
            break
# Run the main function when the script is executed
if __name__ == "__main__":
    main()