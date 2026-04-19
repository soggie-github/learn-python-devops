from socket import timeout
import time
from tracemalloc import start

import requests
from requests.exceptions import HTTPError
import time
from datetime import datetime

def check_apis(urls, threshold):
    results = []

    for url in urls:
        try:
            start = time.time()
            response = requests.get(url)
            elapsed = time.time() - start

            response.raise_for_status()

            if elapsed > threshold:
                status = "SLOW"
            else:
                status = "OK"
        except (HTTPError, requests.RequestException) as e:
            status = "DOWN"
            elapsed = None
        results.append(url, status, elapsed)
    
    return results