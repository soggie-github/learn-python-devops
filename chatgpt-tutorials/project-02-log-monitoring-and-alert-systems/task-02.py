# Log Monitoring and Alert System
from json import dumps
import requests
import time

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

# Function to monitor a log file for new entries containing "ERROR" and send alerts via a webhook
def alert_logs(file_name, alert_type):
    error_logs = []
# Open the file in read mode and search for lines containing the specified alert_type (e.g., "ERROR"). If found, clean the line by stripping whitespace, store it in the error_logs list, and print it to the console. After processing the file, save the alert logs to "alert_logs.txt" using the save_to_file function. If no logs of the specified type are found, write a message indicating that.
    with open(file_name, 'r') as file:
        print(f"\n=== {alert_type} logs ===")

        for line in file:
            if alert_type in line:
                cleaned_line = line.strip()
                error_logs.append(cleaned_line)
                print(cleaned_line)
    # Write the alert logs and summary to a new file named "alert_logs.txt" using the save_to_file function. If no logs of the specified type are found, write a message indicating that.
    save_to_file(
        "alert_logs.txt",
        f"\n=== {alert_type} logs ===",
        error_logs,
        f"No {alert_type} logs found."
    )
    
    print("\nSaved to alert_logs.txt")

    # Return the alert logs as a single string with each log separated by a newline character. If no logs are found, return a message indicating that.
    if error_logs:
        return "\n".join(error_logs)
    else:
        return f"No {alert_type} logs found."

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

        print(response)
        print("DEBUG payload:", payload)

# Function to monitor a log file for new entries containing "ERROR". If an "ERROR" is found, it sends an alert message via the webhook_alert function and saves the alert to "alerts.txt" using the save_to_file function. The function continuously monitors the log file until interrupted by the user (e.g., via a keyboard interrupt).
def monitor_log(file_name):
    with open(file_name, 'r') as file:
        file.seek(0, 2) # Move the cursor to the end of the file
        while True:
            line = file.readline()

            if not line:
                time.sleep(1) # Sleep briefly to avoid busy waiting
                continue
            if "ERROR" in line:
                
                alert_message = f"ALERT: {line.strip()}"
                print(alert_message)

                webhook_alert(alert_message)
                save_to_file(
                    "alerts.txt",
                    "New Alert",
                    [line.strip()],
                    "No alerts"
                )

file_name = input("Enter log file: ")

# Open the file in read mode and search for lines containing "ERROR". If found, clean the line by stripping whitespace, store it in the error_logs list, and print it to the console. After processing the file, save the error logs to "error_logs.txt" using the save_to_file function. If no "ERROR" logs are found, write a message indicating that.
try:
    monitor_log(file_name)
except KeyboardInterrupt:
    print("\nMonitoring stopped.")