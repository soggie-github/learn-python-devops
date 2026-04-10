import os

def input_file():
    # Prompt the user to enter the name of the file and validate its existence using a loop. If the file exists, return the filename; otherwise, print an error message and prompt the user again until a valid file is provided.
    while True:
        filename = input("Enter the name of the file: ")

        # Handle the case where the file does not exist or is not readable
        try: 
        # Check if the file exists and return the filename if it does, otherwise print an error message and prompt again
            if os.path.isfile(filename):
                return filename
            else:
                print(f"Error: The file '{filename}' was not found. Please try again.")
        
        # Handle any other exceptions that may occur during file checking and prompt the user again
        except Exception as e:
            print(f"An error occurred: {e}. Please try again.")
        
def error_logs():


    #   Prompt the user to enter the name of the file and validate its existence using the input_file function
    file_name = input_file()
    error_log_count = 0
    error_logs = []
        
        
    # Open the file in read mode
    with open(file_name, 'r') as file:
        print("\nShow only ERROR logs")
        
        # Iterate through each line in the file and check for lines containing "ERROR". If found, increment the error count, clean the line by stripping whitespace, and store it in the error_logs list. Print each error log to the console.
        for line in file:
            if "ERROR" in line:
                error_log_count += 1

                # Clean the line by stripping leading and trailing whitespace and store it in the error_logs list
                cleaned_line = line.strip()

                # Append the cleaned line to the error_logs list and print it to the console
                error_logs.append(cleaned_line)
                
                print(cleaned_line)

    # Write the error logs and summary to a new file named "log_summary.txt"
    with open("error_logs.txt", 'w') as out_file:
        out_file.write("Show only ERROR logs\n")
        # Write each error log to the file
                
        # If no "ERROR" logs are found, write a message indicating that
        if error_log_count == 0:
            out_file.write("No ERROR logs found.\n")
        else:
            for log in error_logs:
                out_file.write(log + "\n")
    print("\nSaved to error_logs.txt")

        


def all_logs():

    #   Prompt the user to enter the name of the file and validate its existence using the input_file function 
    file_name = input_file()
    log_types = ["ERROR", "WARNING", "INFO"]
    newloglist = []
    all_logs_count = 0

    # Open the file in read mode
    with open(file_name, 'r') as file:
        print("\nShow all logs")

        # Iterate through each line in the file and check for lines containing "ERROR", "WARNING", or "INFO". If found, increment the all_logs_count, clean the line by stripping whitespace, and store it in the newloglist. Print each log to the console.
        for line in file:
            # Check if the line contains any of the log types ("ERROR", "WARNING", "INFO") and if it does, increment the all_logs_count, clean the line by stripping leading and trailing whitespace, store it in the newloglist, and print it to the console
            if any(log in line for log in log_types):
                all_logs_count += 1
                cleaned_line =  line.strip()
                newloglist.append(cleaned_line)
                print(cleaned_line)
            
    # Write the error logs and summary to a new file named "log_summary.txt"
    with open("all_logs.txt", 'w') as out_file:
        out_file.write("Show all logs\n")
        # Write each error log to the file
                
            # If no "ERROR" logs are found, write a message indicating that
        if all_logs_count == 0:
            out_file.write("No logs found.\n")
        else:
            for log in newloglist:
                out_file.write(log + "\n")
    print("\nSaved to all_logs.txt")




def summary_only():
    file_name = input_file()
    prefixes = ["ERROR:", "WARNING:", "INFO:"]
    newloglist = []
    summary_only_count = 0

    # Open the file in read mode
    with open(file_name, 'r') as file:
        print("\nShow summary only")
        for line in file:
            for prefix in prefixes:
                # Check if the line starts with the prefix (e.g., "ERROR:", "WARNING:", "INFO:"). If it does, clean the line by removing the prefix and stripping whitespace, store it in the newloglist, print it to the console, and break out of the inner loop to avoid checking other prefixes for the same line.
                if line.startswith(prefix):
                    summary_only_count += 1
                    #  Clean the line by removing the prefix and stripping leading and trailing whitespace, then store it in the newloglist and print it to the console
                    cleaned_line = line[len(prefix):].strip()
                    # Append the cleaned line to the newloglist and print it to the console
                    newloglist.append(cleaned_line)
                    print(cleaned_line)
                    break


        # Write the error logs and summary to a new file named "log_summary.txt"
    with open("summary_logs.txt", 'w') as out_file:
        out_file.write("Show summary only\n")
        # Write each error log to the file
                
            # If no "ERROR" logs are found, write a message indicating that
        if summary_only_count == 0:
            out_file.write("No logs found.\n")
        else:
            for log in newloglist:
                out_file.write(log + "\n")
    print("\nSaved to summary_logs.txt")

def menu():
    # Display a menu to the user with options to analyze all logs, analyze only ERROR logs, show summary only, or exit the program. Prompt the user to enter their choice and call the corresponding function based on the user's input. If the user enters an invalid choice, display an error message and prompt them again until they enter a valid choice or choose to exit.
    while True:
        print("\nMenu:")
        print("1. Analyze all logs")
        print("2. Analyze only ERROR logs")
        print("3. Show summary only")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            all_logs()
        elif choice == '2':
            error_logs()
        elif choice == '3':
            summary_only()
        elif choice == '4':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 4.")
#   return input_file
menu()