import os
import argparse

def save_to_file(filename, title, logs, empty_message):
    with open(filename, 'w') as out_file:
        out_file.write(title + "\n")
        if not logs:
            out_file.write(empty_message + "\n")
        else:
            for log in logs:
                out_file.write(log + "\n")


        
def error_logs(file_name):

    error_log_count = 0
    error_logs = []
        
        
    # Open the file in read mode
    with open(file_name, 'r') as file:
        print("\n=== ERROR logs ===")
        
        # Iterate through each line in the file and check for lines containing "ERROR". If found, increment the error count, clean the line by stripping whitespace, and store it in the error_logs list. Print each error log to the console.
        for line in file:
            if "ERROR" in line:
                error_log_count += 1

                # Clean the line by stripping leading and trailing whitespace and store it in the error_logs list
                cleaned_line = line.strip()

                # Append the cleaned line to the error_logs list and print it to the console
                error_logs.append(cleaned_line)
                
                print(cleaned_line)

    save_to_file(
        "error_logs.txt",
        "ERROR Logs",
        error_logs,
        "No ERROR logs found"
    )
    print("\nSaved to error_logs.txt")

        


def all_logs(file_name):


    log_types = ["ERROR", "WARNING", "INFO"]
    newloglist = []
    all_logs_count = 0

    # Open the file in read mode
    with open(file_name, 'r') as file:
        print("\n=== Show all logs ===")

        # Iterate through each line in the file and check for lines containing "ERROR", "WARNING", or "INFO". If found, increment the all_logs_count, clean the line by stripping whitespace, and store it in the newloglist. Print each log to the console.
        for line in file:
            # Check if the line contains any of the log types ("ERROR", "WARNING", "INFO") and if it does, increment the all_logs_count, clean the line by stripping leading and trailing whitespace, store it in the newloglist, and print it to the console
            if any(log in line for log in log_types):
                all_logs_count += 1
                cleaned_line =  line.strip()
                newloglist.append(cleaned_line)
                print(cleaned_line)

    save_to_file(
        "all_logs.txt",
        "All Logs",
        newloglist,
        "No logs found"
    )
    print("\nSaved to all_logs.txt")




def summary_only(file_name):

    prefixes = ["ERROR:", "WARNING:", "INFO:"]
    newloglist = []
    summary_only_count = 0

    # Open the file in read mode
    with open(file_name, 'r') as file:
        print("\n=== Show summary only ===")
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

        save_to_file(
        "summary_logs.txt",
        "Summary Logs",
        newloglist,
        "No summary logs found"
    )
    print("\nSaved to summary_logs.txt")



# Use argparse to allow the user to specify the log file and analysis mode (all, error, summary) as command-line arguments. Based on the user's choice, call the corresponding function to perform the analysis and display the results.
parser = argparse.ArgumentParser(description="Log File Analyzer and extract ERROR/WARNING/INFO logs from a log file and save the results to a new file.")

parser.add_argument("--file", required=True, help="Path to the log file to analyze")
parser.add_argument("--mode", required=True, choices=["all", "error", "summary"], default="all", help="Analysis mode (default: all)")
parser.add_argument("--output", help="Output file (optional)")
# 
args = parser.parse_args()

if not os.path.isfile(args.file):
    print(f"Error: File '{args.file}' does not exist.")
    exit(1)

# Based on the user's choice of analysis mode, call the corresponding function to perform the analysis and display the results. If the user selects "all", call the all_logs function; if they select "error", call the error_logs function; if they select "summary", call the summary_only function.
if args.mode == "all":
    all_logs(args.file)
elif args.mode == "error":
    error_logs(args.file)
elif args.mode == "summary":
    summary_only(args.file)