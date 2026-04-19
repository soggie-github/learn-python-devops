# Log Monitoring and Alert System
# Refactor the code to include a function that checks for duplicate error messages and counts their occurrences. 
# If an error message occurs more than a specified threshold with a specific time (10 seconds), 
# print an alert message indicating that the threshold has been reached. 
# This code tracks all errors together, as per message
# Additionally, print a report of all duplicate error messages and their counts after processing the log file.
import requests
import time
from datetime import datetime, timedelta
from collections import deque, Counter
import argparse
import os

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

# Function to send an alert message to a specified webhook URL. 
# If the message is empty, the function will return without sending the alert.
def webhook_alert(app_message):
    url = os.getenv("WEBHOOK_URL")  # Get the webhook URL from an environment variable  
    # Check if log_text is empty before sending the alert. If it is empty, print an error message and return without sending the alert.
    
    if not url:
        print("Error: WEBHOOK_URL environment variable is not set.")
        return
    
    if not app_message:
        return
    
    # Create a payload dictionary with the alert message to be sent to the webhook. 
    # The payload is structured as a JSON object with a "text" field containing the alert message.
    payload = {"text": app_message}

    # Send the alert message to the specified webhook URL using a POST request. If the request is successful, print the status code of the response. If an exception occurs during the request, catch it and print an error message along with the exception details. Additionally, print the response and the payload for debugging purposes.
    try:
        # Send a POST request to the specified webhook URL with the payload as JSON data. The response from the server is stored in the 'response' variable.
        response = requests.post(url, json=payload)
        print(f"webhook sent: {response.status_code}")
    except Exception as e:
        print(f"webhook failed: {e}")
        print("DEBUG payload:", payload)

# Function to parse the timestamp from a log line. 
# It assumes the timestamp is in the format "YYYY-MM-DD HH:MM:SS" and is located at the beginning of the log line. 
# If the timestamp cannot be parsed, it returns None.
def parse_timestamp(log_line):
    try:
        timestamp_text = log_line[:19]  # Assuming the timestamp is in the format "YYYY-MM-DD HH:MM:SS"
        return datetime.strptime(timestamp_text, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None

# Function to check for duplicate error messages 
# in a log file and count their occurrences.
def duplicate_check(file_name, threshold, window_seconds):

    # Define a time window using the specified number of seconds.
    time_window = timedelta(seconds=window_seconds)
    error_counts = Counter()
    recent_error_times = {}  # A dictionary to store timestamps of recent errors for threshold checking
    alerted_errors = set()  # A set to keep track of errors that have already triggered an alert
    
    with open(file_name, 'r') as file:        
        for line in file:
       
            # Check if the line contains "ERROR". 
            # If it does not, skip to the next line. 
            # If it does, clean the line by stripping whitespace, 
            # parse the timestamp, and extract the error message.
            if "ERROR" not in line:
                continue

            cleaned_line = line.strip()

            # Parse the timestamp from the cleaned line using the parse_timestamp function. 
            # If the timestamp cannot be parsed (i.e., if parse_timestamp returns None), skip
            log_time = parse_timestamp(cleaned_line)

            if not log_time:
                continue  # Skip lines with invalid timestamps
            
            # Split the cleaned line on "ERROR:" to extract the error message. 
            # If the split does not result in at least two parts, skip to the next line. 
            # Otherwise, take the second part of the split (the error message), 
            # strip any leading or trailing whitespace, and use it as the error message.
            parts = cleaned_line.split("ERROR:", 1)

            if len(parts) < 2:
                continue  # Skip lines that do not contain a valid error message

            # Extract the error message from the second part of the split and strip any leading or trailing whitespace.
            error_message = parts[1].strip()

            # If this error message is not already in recent_error_times, 
            # initialize a new deque for it. Then, append the current log 
            # time to the deque for this error message. Increment the 
            # count of this error message in the error_counts Counter.
            if error_message not in recent_error_times:
                recent_error_times[error_message] = deque()

            recent_error_times[error_message].append(log_time)
            error_counts[error_message] += 1

            # Remove timestamps from recent_error_times 
            # that are outside the specified time window.
            while (
                recent_error_times[error_message] and 
                (log_time - recent_error_times[error_message][0]) > time_window
            ):
                recent_error_times[error_message].popleft()

            # Check if the number of error occurrences 
            # within the time window exceeds the threshold.
            if len(recent_error_times[error_message]) >= threshold:
                if error_message not in alerted_errors: 
                    alert_message = (
                        f"ALERT: '{error_message}' occurred "
                        f"{len(recent_error_times[error_message])} times within "
                        f"{window_seconds} seconds"
                    )
                    print(alert_message)
                    webhook_alert(alert_message)
                    alerted_errors.add(error_message)  # Mark this error as having triggered an alert

        print("\nDuplicate Error Report")
        print("_" * 30)
        
        # Check for duplicate error messages and print their counts. 
        # If no duplicates are found, print a message indicating that.

        duplicates = {k: v for k, v in error_counts.items() if v > 1}

        if duplicates:
            for error, count in duplicates.items():
                print(f"{error} -> {count} time(s)")
        else:
            print("No duplicate errors found.")

# Function to monitor a log file for new entries containing "ERROR". If an "ERROR" is found, it sends an alert message via the webhook_alert function and saves the alert to "alerts.txt" using the save_to_file function. The function continuously monitors the log file until interrupted by the user (e.g., via a keyboard interrupt).
def monitor_log(file_name, threshold, window_seconds):

    time_window = timedelta(seconds=window_seconds)  # Define a time window for checking duplicate errors   
    recent_error_times = {}  # A dictionary to store timestamps of recent errors for threshold checking 
    alerted_errors = set()  # A set to keep track of errors that have already triggered an alert    

    with open(file_name, 'r') as file:
        file.seek(0, 2) # Move the cursor to the end of the file
        while True:
            line = file.readline()

            if not line:
                time.sleep(1) # Sleep briefly to avoid busy waiting
                continue
            if "ERROR" not in line:
                continue
            
            # Clean the line by stripping whitespace and parse the timestamp. 
            # If the timestamp cannot be parsed (i.e., if parse_timestamp returns None), 
            # skip to the next line.
            cleaned_line = line.strip()
            log_time = parse_timestamp(cleaned_line)

            if not log_time:
                continue  # Skip lines with invalid timestamps
            
            # Split the cleaned line on "ERROR:" to extract the error message. 
            # If the split does not result in at least two parts, skip to the next line. 
            # Otherwise, take the second part of the split (the error message), 
            # strip any leading or trailing whitespace, and use it as the error message.
            parts = line.strip().split("ERROR:", 1)
            if len(parts) < 2:
                continue  # Skip lines that do not contain a valid error message
            
            error_message = parts[1].strip()

            # If this error message is not already in recent_error_times, initialize a new deque for it. Then, append the current log time to the deque for this error message.
            if error_message not in recent_error_times:
                recent_error_times[error_message] = deque()
            recent_error_times[error_message].append(log_time)

            # Remove timestamps from recent_error_times that are outside the specified time window.
            while (
                recent_error_times[error_message] and
                (log_time - recent_error_times[error_message][0]) > time_window
            ):
                # Remove timestamps from recent_error_times that are outside the specified time window.
                recent_error_times[error_message].popleft()

            # Check if the number of error occurrences within the time window exceeds the threshold. If it does and an alert has not already been triggered for this error message, print an alert message, send it via the webhook_alert function, and save it to "alerts.txt" using the save_to_file function. Mark this error message as having triggered an alert to avoid duplicate alerts for the same error message.
            if len(recent_error_times[error_message]) >= threshold:
                if error_message not in alerted_errors: 
                    alert_message = (
                        f"ALERT: '{error_message}' occurred "
                        f"{len(recent_error_times[error_message])} times within "
                        f"{window_seconds} seconds"
                    )
                    print(alert_message)
                    webhook_alert(alert_message)
                    alerted_errors.add(error_message)  # Mark this error as having triggered an alert

                    save_to_file(
                        "alerts.txt", 
                        "New Alert", 
                        [alert_message], 
                        "No new alerts."
                        )
                    alerted_errors.add(error_message)  # Mark this error as having triggered an alert   

# Use argparse to allow the user to specify the log file and analysis mode (all, error, summary) as command-line arguments. Based on the user's choice, call the corresponding function to perform the analysis and display the results.
def parse_arguments():
    parser = argparse.ArgumentParser(description="Monitor a log file for new entries containing 'ERROR' and send alerts via webhook. Also provides options to analyze logs for duplicates and summaries.")
    parser.add_argument("--file", required=True, help="Path to the log file to analyze")
    parser.add_argument("--threshold", type=int, default=5, help="Number of errors required to trigger an alert")
    parser.add_argument("--window", type=int, default=10, help="Time window in seconds for the threshold check (default: 10 seconds)")
    parser.add_argument("--mode", choices=["monitor", "analyze"], default="monitor", help="Mode of operation: 'monitor' to continuously monitor the log file, 'analyze' to analyze the log file for duplicate errors and counts")
    return parser.parse_args()

def main():
    args = parse_arguments()

    # Check if the specified log file exists. If it does not, print an error message and exit the program.
    if not os.path.isfile(args.file):
        print(f"Error: File '{args.file}' does not exist.")
        exit(1)    
    
    # Based on the mode specified by the user, 
    # call the appropriate function to either analyze the log file for 
    # duplicate errors and counts or to continuously monitor the log file 
    # for new error entries and send alerts when the threshold is reached.
    if args.mode == "analyze":
        duplicate_check(args.file, threshold=args.threshold, window_seconds=args.window)    
    elif args.mode == "monitor":
        monitor_log(args.file, threshold=args.threshold, window_seconds=args.window)
        
# The main function serves as the entry point of the program. 
# It parses command-line arguments to determine the log file 
# to analyze, the threshold for triggering alerts, the time window 
# for checking duplicate errors, and the mode of operation (monitoring or analyzing). 
# Based on the user's choice, it calls the appropriate function 
# to perform the desired analysis or monitoring of the log file.

if __name__ == "__main__":
    try:
        main()
        # Call the duplicate_check function to analyze the log file 
        # for duplicate error messages and alert if the threshold is reached.
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")