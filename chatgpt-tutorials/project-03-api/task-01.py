import requests
from requests.exceptions import HTTPError, Timeout
import time

def check_api(urls):
   for url in urls:
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"Other error occurred: {err}")
        except Timeout:
            print("The request timed out")
        else:
            print("Success!")
