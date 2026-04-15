#def file_input():
#    input_file = input("Enter the name of the file: ")
#    # Check if the file exists and is readable
#    return input_file

def analyze_log():
    while True:
        filename = input("Enter the name of the file: ")
            
        try:                
            # Initialize counters for each log level
            info_count = 0
            warning_count = 0
            error_count = 0
            error_logs = []

            # Open the file in read mode
            with open(filename, 'r') as file:
                print("\nERROR Log:")
            
                # Iterate through each line in the file and count the occurrences of "ERROR", "WARNING", and "INFO"
                for line in file:
                    # Check if the line contains "ERROR", "WARNING", or "INFO" and update the respective counters
                    if "ERROR" in line:
                        error_count += 1
                        print(line.strip())  # Print the line containing "ERROR"
                        cleaned_line = line.strip()
                        error_logs.append(cleaned_line)

                    if "WARNING" in line:
                        warning_count += 1

                    if "INFO" in line:
                        info_count += 1

            # Write the error logs and summary to a new file named "log_summary.txt"
            with open("log_summary.txt", 'w') as out_file:
                out_file.write("ERROR Log :\n")
                # Write each error log to the file
                
                # If no "ERROR" logs are found, write a message indicating that
                if error_count == 0:
                    out_file.write("No ERROR logs found.\n")
                else:
                    for log in error_logs:
                        out_file.write(log + "\n")

                # Write the summary of log counts to the file
                out_file.write("\nLog Summary:\n")
                out_file.write(f"ERROR: {error_count}\n")
                out_file.write(f"WARNING: {warning_count}\n")
                out_file.write(f"INFO: {info_count}\n")

            # If no "ERROR" logs are found, print a message indicating that            
            if error_count == 0:
                print("No ERROR logs found.")

            print("\nLog Summary:")
            print("ERROR: ", error_count)
            print("WARNING: ", warning_count)
            print("INFO: ", info_count)

            break  # Exit the loop after successful analysis
            
        except FileNotFoundError:
            print(f"Error: The file '{filename}' was not found.")
        
# Call the function to analyze the log file
analyze_log()