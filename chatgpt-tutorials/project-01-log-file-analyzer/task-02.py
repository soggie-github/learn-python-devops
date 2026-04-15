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

            # Open the file in read mode
            with open(filename, 'r') as file:

                # Iterate through each line in the file and count the occurrences of "ERROR", "WARNING", and "INFO"
                for line in file:
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

            break  # Exit the loop after successful analysis
            
        except FileNotFoundError:
            print(f"Error: The file '{filename}' was not found.")
        
# Call the function to analyze the log file
analyze_log()