import time
import requests
from requests.exceptions import HTTPError, RequestException, Timeout


def check_apis(urls, threshold, timeout=5.0):
    """
    The check_apis function takes a list of URLs, a response time threshold,
    and an optional timeout value. It checks the response time of each URL 
    by sending a GET request and categorizes the status of each URL as "OK", 
    "SLOW", or "DOWN" based on the response time and any errors encountered.
    The function returns a list of tuples, where each tuple contains the URL,
    its status, and the elapsed time for the request. The status is determined
    as follows:
    - "OK": The request was successful and the response time is within the threshold.
    - "SLOW": The request was successful but the response time exceeds the threshold.
    - "DOWN": The request failed due to an error or timeout.
    """
    results = []

    for url in urls:
        try:
            start = time.time()
            response = requests.get(url, timeout=timeout)
            elapsed = time.time() - start

            response.raise_for_status()

            if elapsed > threshold:
                status = "SLOW"
            else:
                status = "OK"
        except (HTTPError, Timeout, RequestException) :
            status = "DOWN"
            elapsed = None
        results.append((url, status, elapsed))
    
    return results
