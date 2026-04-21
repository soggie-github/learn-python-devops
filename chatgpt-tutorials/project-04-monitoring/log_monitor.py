from collections import Counter
from pathlib import Path


# This module provides functionality to monitor log files for error 
# patterns and generate alerts when certain thresholds are exceeded.  
def _extract_error_key(line):
    """
    The _extract_error_key function takes a line of text as input and 
    attempts to extract an error key from it. It checks if the line 
    contains the substring "ERROR:". If it does, it splits the line at 
    the first occurrence of "ERROR:" and returns the part after "ERROR:" 
    as the error key, stripped of any leading or trailing whitespace. 
    If the line does not contain "ERROR:", the function returns None. 
    This function is used to identify and extract specific error keys 
    from log lines for further processing in the log monitoring system.
    """
    text = line.strip()
    parts = text.split("ERROR:", 1)
    if len(parts) < 2:
        return None
    return parts[1].strip()



def check_logs(log_files, error_limit, state=None):
    """
        The check_logs function takes a list of log file paths, 
        an error limit, and an optional state dictionary. 
        It reads the log files, extracts error keys from lines 
        containing "ERROR", and counts their occurrences. 
        If the count of a specific error key reaches the defined 
        error limit, an alert message is generated. The function 
        returns a list of alert messages and the updated state 
        dictionary, which includes offsets for each log file and 
        counts of error occurrences. The state is used to keep 
        track of the last read position in each log file and the 
        count of each error key across multiple calls to the function, 
        allowing it to monitor logs continuously without reprocessing 
        previously read lines.    
    """
    if state is None:
        # Initialize the state dictionary with default values if it is 
        # not provided. The state dictionary contains two keys: 
        # "offsets" and "counts". "offsets" is a dictionary that 
        # will store the last read position for each log file, 
        # while "counts" is a Counter object that will keep track 
        # of the count of each error key encountered in the log files.
        state = {"offsets": {}, "counts": Counter()}

    # Ensure that the "offsets" key in the state dictionary is 
    # initialized as an empty dictionary if it does not already exist. 
    # This is done using the setdefault method, which sets the value of 
    # "offsets" to an empty dictionary if it is not already present in the 
    # state. The "counts" key is also initialized as a Counter object, 
    # which will be used to count occurrences of error keys. If "counts" 
    # is already present in the state but is not a Counter object, it will 
    # be converted to a Counter.
    offsets = state.setdefault("offsets", {})
    counts_obj = state.get("counts", {})
    if isinstance(counts_obj, Counter):
        counts = counts_obj
    else:
        counts = Counter(counts_obj)
    state["counts"] = counts

    alerts = []

    for file_name in log_files:
        path = Path(file_name)

        try:
            if not path.exists():
                continue

            # Open the log file for reading with UTF-8 encoding and error handling. 
            # The file is opened in read mode, and the encoding is set to "utf-8" 
            # to ensure that it can handle a wide range of characters. The errors 
            # parameter is set to "replace" to replace any characters that cannot 
            # be decoded with a placeholder character, preventing the program from 
            # crashing due to encoding issues. Before seeking to the last saved
            # position, validate that the stored offset is not beyond the current
            # end of the file so log truncation or rotation does not cause the
            # monitor to miss new content. If any filesystem-related error occurs
            # while checking, opening, reading, or updating the file position,
            # skip that file and continue monitoring the others.
            with path.open("r", encoding="utf-8", errors="replace") as file:
                stored_offset = offsets.get(file_name, 0)
                file.seek(0, 2)
                current_size = file.tell()

                if stored_offset > current_size:
                    stored_offset = 0

                file.seek(stored_offset)

                for line in file:
                    key = _extract_error_key(line)
                    if key is None:
                        continue

                    counts[key] += 1
                    if counts[key] == error_limit:
                        alerts.append(
                            f"ALERT ERROR LIMIT '{key}' occurred {counts[key]} times"
                        )
                offsets[file_name] = file.tell()
        except (OSError, IOError):
            continue
    return alerts, state
