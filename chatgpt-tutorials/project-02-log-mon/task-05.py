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
    url = "https://chat.googleapis.com/v1/spaces/AAQAAYSBTcY/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=0owxwWYEY9j9bXdaAnCXZKrf7NZvamqd0fWn2YLxRLw"
    
    # Check if log_text is empty before sending the alert. If it is empty, print an error message and return without sending the alert.
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
def duplicate_check(file_name, threshold=5, window_seconds=10):
       
       
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
            log_time = parse_timestamp(cleaned_line)

            if not log_time:
                continue  # Skip lines with invalid timestamps

            parts = cleaned_line.split("ERROR:", 1)
            if len(parts) < 2:
                continue  # Skip lines that do not contain a valid error message

            error_message = parts[1].strip()

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
                        f"ALERT: {error_message} occurred within 10 seconds "
                        f"at {len(recent_error_times[error_message])} times in {window_seconds}s"
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

                 
file_name = input("Enter log file: ")


try:
    # Call the duplicate_check function to analyze the log file 
    # for duplicate error messages and alert if the threshold is reached.
    duplicate_check(file_name)
except KeyboardInterrupt:
    print("\nMonitoring stopped.")