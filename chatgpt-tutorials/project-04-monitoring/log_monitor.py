import time
from collections import Counter


def check_logs(file_name):
    #rcecent_error_times = {}
    #alerted_errors = set()
    error_counts = Counter()


    with open(file_name, 'r') as file:
        #file.seek(0, 2)
        while True:
            line = file.readline()

            if not line:
                time.sleep(1)
                continue

            if "ERROR" in line:
                cleaned_line = line.strip()
                alert_message = f"ALERT: {cleaned_line}"
                print(alert_message)
                
                error_counts[cleaned_line] += 1
                if error_counts[cleaned_line] == 1:
                    print(f"First occurrences of this error: {cleaned_line}")
                else:
                    print(f"Duplicate count for this error: {error_counts[cleaned_line]} time(s): {cleaned_line}")


check_logs("logs.txt")