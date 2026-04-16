import requests
from requests.exceptions import HTTPError, Timeout
import time
from datetime import datetime
import argparse
import os
from colorama import Fore, Style, init

# Initialize Colorama
init()

""" 
    CLI cmmandline API Monitor Tool for terminal dashboard (live-updating screen) that checks the status and response time of 
    each API and alerts if any API is down or slow. results are saved to a file with a timestamp. 
    The tool accepts a list of API URLs, a slow response threshold, and a check interval as command-line arguments.
    It runs indefinitely until interrupted by the user. Add Color Output
    OK → green  
SLOW → yellow  
DOWN → red  
"""
# Function to clear the terminal screen based on the operating system
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to check the status and response time of each API
def check_apis(urls, threshold, timeout):
    results = []

    # Iterate through the list of URLs and make a GET request to each one
    for url in urls:
        try:
            # Record the start time, make the GET request, 
            # and record the end time
            start = time.time()
            response = requests.get(url, timeout=timeout)
            
            elapsed = time.time() - start

            # Raise an HTTPError if the response status code indicates an error (4xx or 5xx)
            response.raise_for_status()
    
            # Check if the response time exceeds the slow threshold and print the appropriate message   
            if elapsed >  threshold:
                status = "SLOW"                    
            else:
                status = "OK"
        except (HTTPError, Timeout, requests.RequestException) as e:
            status = "DOWN"
            elapsed = None
        # Append the URL, status, and response time (if available) to the results list as a tuple.
        results.append((url, status, elapsed))
    
    return results
        
# Function to display the dashboard with the status and response time of each API in a formatted manner
def display_dashboard(results):
    # Print the dashboard header with the current time 
    # and column titles for API, status, and response time.
    print("=" * 70)
    print("API MONITOR DASHBOARD")
    print("=" * 70)
    print(f"TIME: {datetime.now().strftime('%H:%M:%S')}")
    print("_" * 70)
    print(f"{'API':30} {'STATUS':25} {'TIME'}")
    print("_" * 70)

    # Iterate through the results and print the URL, status, 
    # and response time for each API in a formatted manner.  
    for url, status, elapsed in results:
        # Shorten the URL for display if it's too long and format 
        # the response time to two decimal places if available.
        short_url = url[:28] + ".." if len(url) > 30 else url

        # Format the response time to two decimal places if available, 
        # otherwise display an underscore
        time_display = f"{elapsed:.2f}s" if elapsed else "_"

        # Set the color based on the status of the API (OK, SLOW, DOWN) 
        # and print the information in a formatted manner with color coding.
        if status == "OK":
            color = Fore.GREEN
        elif status == "SLOW":
            color = Fore.YELLOW 
        else:
            color = Fore.RED
        
        print(f"{short_url:30}", color + f"{status:25}" + Style.RESET_ALL, time_display)

    print("_" * 70)
    
    

    # Calculate the summary of OK, SLOW, and DOWN APIs by 
    # counting the occurrences of each status in the results 
    # list and print the summary with color coding for alerts if any API is down. 
    ok = sum(1 for _, s, _ in results if s == "OK")
    slow = sum(1 for _, s, _ in results if s == "SLOW")
    down = sum(1 for _, s, _ in results if s == "DOWN")

    print(f"\nSummary --> OK={ok} | SLOW={slow} | DOWN={down}")

    # If any API is down, print an alert message in red color.
    if down > 0:
        print(Fore.RED + "ALERT: Some APIs are DOWN!" + Style.RESET_ALL)
    

def parse_arguments():
    # Create an argument parser to allow users to specify 
    # the slow response threshold and check interval
    parser = argparse.ArgumentParser(description="Monitoring the status and response time of each API ")
    parser.add_argument("--urls", required=True, help="Comma-separated list of API URLs to monitor")
    parser.add_argument("--threshold", type=float, default=1.5, help="Slow response threshold in seconds")
    parser.add_argument("--interval", type=int, default=5, help="Check interval in seconds")
    parser.add_argument("--timeout", type=int, default=5, help="Request timeout in seconds")
    return parser.parse_args()

def main():

    # Parse command-line arguments using the parse_arguments function to get the list of URLs, 
    # slow response threshold, check interval, and request timeout.
    args = parse_arguments()

    # Split the comma-separated list of URLs into a list
    urls = []
    parts = args.urls.split(",")
    for url in parts:
        urls.append(url.strip())
    
    # Run the monitoring loop indefinitely until interrupted by the user
    while True:
        try:
            clear_screen()
            print(f"\nNext check in {args.interval}s...")
            results = check_apis(urls, args.threshold, args.timeout)
            display_dashboard(results)
            time.sleep(args.interval)
            
        except KeyboardInterrupt:
            print("\nMonitoring stopped")
            break
        print(f"\nNext check in {args.interval}s...")
# Run the main function when the script is executed
if __name__ == "__main__":
    main()