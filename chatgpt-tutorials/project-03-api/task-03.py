import requests
from requests.exceptions import HTTPError, Timeout
import time
from datetime import datetime
import argparse

""" 
    CLI cmmandline API Monitor Tool that checks the status and response time of 
    each API and alerts if any API is down or slow. 
    It runs indefinitely until interrupted by the user.   
"""


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


    success = 0
    slow = 0
    fail = 0

    # Iterate through the list of URLs and make a GET request to each one
    for url in urls:
       
        try:
            

            # Record the start time, make the GET request, 
            # and record the end time
            start = time.time()
            response = requests.get(url, timeout=timeout)
            end = time.time()
            elapsed = end - start

            response.raise_for_status()
    


            # Check if the response time exceeds the slow threshold and print the appropriate message   
            if elapsed >  threshold:
                slow += 1
                print(f"ALERT: {url} -> SLOW ({response.status_code}) - ({elapsed:.3f}s)")
    
            else:

                success += 1
                print(f"{url} -> OK {response.status_code} - {elapsed:.3f}s")
            

        except Timeout:
            fail += 1
            print(f"ALERT: {url} -> TIMEOUT")
        except HTTPError as http_err:
            fail += 1
            print(f"ALERT: {url} -> HTTP ERROR: {http_err}")
        except Exception as err:
            fail += 1
            print(f"ALERT: {url} -> ERROR: {err}")
        


    summary = (f"\nSummary: OK={success}, SLOW={slow}, FAIL={fail}")
    print(summary)
    save_to_file(
            "alerts.txt", 
            "Summary Report", 
            [summary], 
            "No new Summary."
        )


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

            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Checking APIs...")
            print("-" * 50)

            # Check the status and response time of each API and alert if any API is down or slow
            check_apis(urls, args.threshold, args.timeout)   

            time.sleep(interval)

        except KeyboardInterrupt:
            print("\nMonitoring stopped")
            break






# Run the main function when the script is executed
if __name__ == "__main__":
    main()