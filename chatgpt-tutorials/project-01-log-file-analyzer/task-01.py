def analyze_log():
    # Initialize counters for each log level
    info_count = 0
    warning_count = 0
    error_count = 0

    # Open the file in read mode
    with open('log.txt', 'r') as file:
        lines = file.readlines()

    # Iterate through each line in the file and count the occurrences of "ERROR", "WARNING", and "INFO"
    for line in lines:
        # Check if the line contains "ERROR", "WARNING", or "INFO" and update the respective counters
        if "ERROR" in line:
            error_count += 1
        if "WARNING" in line:
            warning_count += 1
        if "INFO" in line:
            info_count += 1

    print("\nLog Summary:")
    print("ERROR: ", error_count)
    print("WARNING: ", warning_count)
    print("INFO: ", info_count)

# Call the function to analyze the log file
analyze_log()
