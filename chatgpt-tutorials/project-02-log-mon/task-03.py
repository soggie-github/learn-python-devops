# Log Monitoring and Alert System
# Refactor the code to include a function that checks for duplicate error messages and counts their occurrences. 
# If an error message occurs more than a specified threshold, print an alert message indicating that the threshold has been reached. 
# Additionally, print a report of all duplicate error messages and their counts after processing the log file.
import requests
import time
from collections import Counter



# Function to save logs to a file with a title and handle empty log lists
def save_to_file(file_name, title, logs, empty_message):
# Open the file in append mode and write the title, logs, or an empty message if no logs are found. Each log is written on a new line.
    with open(file_name, 'a') as  out_file:
        out_file.write(title + "\n")
        if not logs:
            out_file.write(empty_message + "\n")
        else:
            for log in logs:
                out_file.write(log + "\n")


# Function to send an alert message to a specified webhook URL. If the message is empty, the function will return without sending the alert.
def webhook_alert(app_message):
    url = "https://chat.googleapis.com/v1/spaces/AAQAAYSBTcY/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=0owxwWYEY9j9bXdaAnCXZKrf7NZvamqd0fWn2YLxRLw"
    
    # Check if log_text is empty before sending the alert. If it is empty, print an error message and return without sending the alert.
    if not app_message:
        return
    
    payload = {"text": app_message}

    # Send the alert message to the specified webhook URL using a POST request. If the request is successful, print the status code of the response. If an exception occurs during the request, catch it and print an error message along with the exception details. Additionally, print the response and the payload for debugging purposes.
    try:
        response = requests.post(url, json=payload)
        print(f"webhook sent: {response.status_code}")
    except Exception as e:
        print(f"webhook failed: {e}")
        print("DEBUG payload:", payload)
"""
# Function to monitor a log file for new entries containing "ERROR". If an "ERROR" is found, it sends an alert message via the webhook_alert function and saves the alert to "alerts.txt" using the save_to_file function. The function continuously monitors the log file until interrupted by the user (e.g., via a keyboard interrupt).
def monitor_log(file_name, alert_to_check=None):
    with open(file_name, 'r') as file:

        error_counts = Counter()
        #file.seek(0, 2) # Move the cursor to the end of the file
        threshold = 5

        while True:
            line = file.readline()

            if not line:
                time.sleep(1) # Sleep briefly to avoid busy waiting
                continue
            if "ERROR" in line:
                cleaned_line = line.strip()
                alert_message = f"ALERT: {cleaned_line}"
                print(alert_message)
            
            
                webhook_alert(alert_message)
                save_to_file(
                    "alerts.txt",
                    "New Alert",
                    [cleaned_line],
                    "No alerts"
                )
                
                error_counts[cleaned_line] += 1
                if error_counts[cleaned_line] == 1:
                    print(f"First occurrence of this error: {cleaned_line}")
                else:
                    print(f"Duplicate count for this error: {error_counts[cleaned_line]} time(s): {cleaned_line}")
"""
def duplicate_check(file_name):
       error_counts = Counter()
       threshold = 5
       with open(file_name, 'r') as file:

        
        #file.seek(0, 2) # Move th cursor to the end of the file
        for line in file:
            if "ERROR" in line:
                cleaned_line = line.strip()


                error_message = cleaned_line.split("ERROR:", 1)[1].strip()
                error_counts[error_message] += 1
                print(f"ERROR: {error_message} | Count: {error_counts[error_message]}")

                if error_counts[error_message] == threshold:
                    print(f"THRESHOLD ALERT: '{error_message}' has occurred {error_counts[error_message]} time(s)")
        print("\nDuplicate Error Report")
        print("_" * 30)
        
        found_duplicates = False

        for error, count in error_counts.items():
            if count > 1:
                found_duplicates = True
                print(f"{error} - > {count} time(s)")
            
            if not found_duplicates:
                 print(f"No duplicate errors found.")

                 
file_name = input("Enter log file: ")

# Open the file in read mode and search for lines containing "ERROR". If found, clean the line by stripping whitespace, store it in the error_logs list, and print it to the console. After processing the file, save the error logs to "error_logs.txt" using the save_to_file function. If no "ERROR" logs are found, write a message indicating that.
try:
    duplicate_check(file_name)
except KeyboardInterrupt:
    print("\nMonitoring stopped.")