import requests
from requests.exceptions import HTTPError, Timeout
import time

def check_api(urls):
    # Iterate through the list of URLs and make a GET request to each one
    for url in urls:
       
        try:
            # Record the start time, make the GET request, and record the end time
            start = time.time()
            response = requests.get(url, timeout=5)
            end = time.time()
            elapsed = end - start 
            response.raise_for_status()

            print(f"{url} -> {response.status_code} {elapsed:.3f} seconds")
        except Timeout:
            print("The request timed out")
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"Other error occurred: {err}")

        else:
            print("Success!")

check_api(["https://api.github.com", "http://colormind.io/api/"])