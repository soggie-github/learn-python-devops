# Log Monitoring and Alert System
import time

def monitor_log(file_name):
    with open(file_name, 'r') as file:
        file.seek(0, 2) # Move the cursor to the end of the file
        while True:
            line = file.readline()

            if not line:
                time.sleep(1) # Sleep briefly to avoid busy waiting
                continue
            if "ERROR" in line:
                print(f"ALERT: {line.strip()}")

monitor_log("logs.txt")