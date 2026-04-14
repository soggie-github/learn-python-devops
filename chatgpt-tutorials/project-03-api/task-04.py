import requests
from requests.exceptions import HTTPError, Timeout
import time
from datetime import datetime
import argparse
import os

""" 
    CLI cmmandline API Monitor Tool that checks the status and response time of 
    each API and alerts if any API is down or slow. 
    It runs indefinitely until interrupted by the user.   
"""
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to save logs to a file with a title and handle empty log lists
def save_to_file(file_name, title, logs, empty_message):
# Open the file in append mode and write the title, logs, or an empty message if no logs are found. 
# Each log is written on a new line.
    with open(file_name, 'a') as  out_file:
        out_file.write(title + "\n")
        
        # If the logs list is empty, write the empty_message to the file. Otherwise, write each log entry on a new line.
        if not logs:
            out_file.write(empty_message + "\n")
        else:
            # Write each log entry from the logs list to the file, followed by a newline character.
            for log in logs:
                out_file.write(log + "\n")

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

            response.raise_for_status()
    


            # Check if the response time exceeds the slow threshold and print the appropriate message   
            if elapsed >  threshold:
                status = "SLOW"                    
            else:
                status = "OK"

        except:
            status = "DOWN"
            elapsed = None
        
        results.append((url, status, elapsed))
    
    return results
        


def display_dashboard(results):
    print(f"TIME: {datetime.now().strftime('%H:%M:%S')}")
    print("_" * 70)
    print(f"{'API':30} {'STATUS':25} {'TIME'}")
    print("_" * 70)

    for url, status, elapsed in results:
        time_display = f"{elapsed:.2f}s" if elapsed else "_"
        print(f"{url:30} {status:25} {time_display}")
    print("_" * 70)


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

    # 
    args = parse_arguments()

    # Get the check interval from the command-line arguments
    interval = args.interval

    # Split the comma-separated list of URLs into a list
    urls = []
    parts = args.urls.split(",")
    for url in parts:
        urls.append(url.strip())
    


    # Run the monitoring loop indefinitely until interrupted by the user
    while True:
        try:
            clear_screen()

            results = check_apis(urls, args.threshold, args.timeout)
            display_dashboard(results)
            time.sleep(args.interval)

        except KeyboardInterrupt:
            print("\nMonitoring stopped")
            break








# Run the main function when the script is executed
if __name__ == "__main__":
    main()