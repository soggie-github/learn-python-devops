import argparse
import json
import time
from pathlib import Path
from alerts import alert
from api_monitor import check_apis
from log_monitor import check_logs

def parse_arguments():
    """
    The parse_arguments function uses the argparse library to define 
    and parse command-line arguments for the monitoring script. It creates 
    an ArgumentParser object, adds a required argument for the configuration 
    file path, and returns the parsed arguments. The function ensures that the
    user provides a valid path to the configuration file when running the script, 
    allowing it to load the necessary settings for API and log monitoring. The 
    expected usage of the script is to run it from the command line with the --config 
    flag followed by the path to the config.json file, which contains the monitoring
    configuration. If the required argument is not provided, the parser will display 
    an error message and exit. The function also includes a description of the script's 
    purpose for better clarity when using the help option.
    """
    parser = argparse.ArgumentParser(description="API + log monitoring")
    parser.add_argument("--config", required=True, help="Path to config.json")
    
    return parser.parse_args()

def load_config(config_path):
    """
    The load_config function reads a JSON configuration file from the 
    specified path, validates the presence of required keys, and sets 
    default values for optional keys. It returns the configuration as a dictionary.
    The function first opens the configuration file in read mode with UTF-8 encoding
    and loads its contents into a dictionary using json.load(). It then checks for 
    the presence of required keys ("apis", "logs", "threshold", "interval", "error_limit")
    in the loaded configuration. If any required keys are missing, it raises a ValueError 
    with a message indicating which keys are missing. Finally, it sets a default value of 
    5 for the "timeout" key if it is not already present in the configuration and returns 
    the validated and updated configuration dictionary.
    """

    with open(config_path, "r", encoding="utf-8") as file:
        config = json.load(file)
    
    required = ["apis", "logs", "threshold", "interval", "error_limit"]
    missing = [key for key in required if key not in config]

    if missing:
        raise ValueError(f"Missing config keys: {', '.join(missing)}")
    config.setdefault("timeout", 5)
    return config

def print_cycle_summary(api_results, log_alert_count):
    """
    The print_cycle_summary function takes the results of API checks and 
    the count of log alerts, and prints a summary of the monitoring cycle. 
    It counts the number of APIs that are "OK", "SLOW", and "DOWN" based on 
    the status in the api_results list, and then prints a summary message that 
    includes these counts along with the number of new log alerts generated in 
    the current cycle. This function provides a concise overview of the monitoring 
    results for each cycle, allowing users to quickly assess the status of their 
    APIs and logs.
    """
    ok = sum(1 for _, status, _ in api_results if status == "OK")
    slow = sum(1 for _, status, _ in api_results if status == "SLOW")
    down = sum(1 for _, status, _ in api_results if status == "DOWN")
    print(f"Summary: OK={ok} SLOW={slow} DOWN={down} NEW_ERROR_ALERTS={log_alert_count}")

def main():
    """
    The main function serves as the entry point for the monitoring script. 
    It parses command-line arguments to obtain the configuration file path, 
    loads the configuration, and initializes the state for log monitoring. 
    The function then enters an infinite loop where it performs API checks 
    and log checks based on the loaded configuration. For each cycle, it 
    collects alerts for any APIs that are down or slow, as well as any new 
    log alerts generated from the log files. It prints each alert message 
    and sends it using the alert function. After processing the results of 
    each cycle, it prints a summary of the API statuses and new log alerts 
    before sleeping for a specified interval before starting the next cycle. 
    The function also includes error handling to allow graceful shutdown when 
    interrupted by a keyboard signal (Ctrl+C).
    """
    args = parse_arguments()
    config = load_config(args.config)

    log_state = {"offsets": {}, "counts": {}}
    print(f"Starting monitor with config: {Path(args.config).resolve()}")

    while True:
        api_results = check_apis(
            config["apis"],
            config["threshold"],
            config["timeout"],
        )
        alerts_to_send = []

        for url, status, elapsed in api_results:
            if status == "DOWN":
                alerts_to_send.append(f"ALERT API DOWN: {url}")
            elif status == "SLOW":
                alerts_to_send.append(
                    f"ALERT API SLOW: {url} took {elapsed:.2f}s > {config['threshold']:.2f}s"
                )

        log_alerts, log_state = check_logs(
            config["logs"],
            config["error_limit"],
            state=log_state,
        )

        alerts_to_send.extend(log_alerts)

        for message in alerts_to_send:
            print(message)
            alert(message)

        print_cycle_summary(api_results, len(log_alerts))
        time.sleep(config["interval"])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nMonitoring stopped")