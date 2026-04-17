
import requests
from requests.exceptions import HTTPError, Timeout
import time
from datetime import datetime
import argparse
from rich.live import Live
from rich.table import Table

""" 
    CLI cmmandline API Monitor Tool for terminal dashboard (live-updating screen) that checks the 
    status and response time of each API and alerts if any API is down or slow. results are saved 
    to a file with a timestamp. The tool accepts a list of API URLs, a slow response threshold, and 
    a check interval as command-line arguments.It runs indefinitely until interrupted by the user. 
    Add Color Output
    
    OK → green  
    SLOW → yellow  
    DOWN → red  
"""

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

# Function to display the dashboard with the 
# status and response time of each API in a formatted manner
def dashboard_ui_table(results, threshold, timeout) -> Table:
    """Make a new table  with the results and 
        return it to be displayed in the live dashboard."""
    
    # Create a new table with the results and return it to be displayed in the live dashboard.
    table = Table(title=f"API Monitor | {datetime.now().strftime('%d/%m/%y - %H:%M:%S')} | threshold={threshold:.2f}s | timeout={timeout}s")
    table.add_column("URL", overflow="fold")
    table.add_column("STATUS", justify="center")
    table.add_column("Response Time", justify="right")

    # Count the number of OK, SLOW, and DOWN statuses to display a summary at the end of the table.
    ok = slow = down = 0

    # Iterate through the results and add a row to the table for each API,
    # with the URL, status (colored based on the status), and response time (if available).
    for url, status, elapsed in results:
        if status == "OK":
            style = "green"
            ok += 1
        elif status == "SLOW":
            style = "yellow"
            slow += 1
        else:
            style = "red"
            down += 1

        # Format the response time to two decimal places if available, 
        # otherwise display a dash to indicate that the response time is not available.    
        time_display = f"{elapsed:.2f}s" if elapsed is not None else "-"

        # Add a row to the table with the URL, colored status, and response time (if available).
        table.add_row(url, f"[{style}]{status}[/{style}]", time_display)

    # Add a summary row at the end of the table with the counts of 
    # OK, SLOW, and DOWN statuses colored based on the status. 
    # The summary row provides a quick overview of the overall status of the monitored APIs.
    table.add_section()
    table.add_row("Summary", f"[green]{ok} OK[/green] | [yellow]{slow} SLOW[/yellow] | [red]{down} DOWN[/red]", "")    
    return table

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
    
    # Check if the list of URLs is empty after parsing and 
    # raise an error if no valid URLs are provided.
    if not urls:
        raise ValueError("No valid URLs provided in --urls")
    
    try:
        # Use the Live context manager from the rich library to 
        # create a live-updating dashboard in the terminal.
        with Live(refresh_per_second=4, screen=True) as live:

            while True:
                # Call the check_apis function to get the status and response 
                # time of each API, and then update the live dashboard with 
                # the new results using the dashboard_ui_table function to create 
                # a new table with the results and display it in the live dashboard.
                results = check_apis(urls, args.threshold, args.timeout)
                live.update(dashboard_ui_table(results, args.threshold, args.timeout))           
                time.sleep(args.interval)
            
    except KeyboardInterrupt:
        print("\nMonitoring stopped")

# Run the main function when the script is executed
if __name__ == "__main__":
    main()