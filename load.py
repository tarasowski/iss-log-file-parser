import os

import os
from datetime import datetime

def load_all_logs(logs_folder, start_date=None, end_date=None):
    """
    Load all log entries from files in the specified folder
    that are within the provided date range.

    Args:
        logs_folder (str): The path to the folder containing log files.
        start_date (datetime, optional): The start date for filtering logs.
        end_date (datetime, optional): The end date for filtering logs.

    Returns:
        list: A list of log entries within the specified date range.
    """
    all_entries = []
    # List only files in the logs folder, exclude directories
    log_files = [f for f in os.listdir(logs_folder) if os.path.isfile(os.path.join(logs_folder, f))]

    for log_file in log_files:
        file_path = os.path.join(logs_folder, log_file)
        # Attempt to open the file with a fallback encoding
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    # Skip comment lines starting with '#'
                    if line.startswith("#"):
                        continue

                    # Assuming the date is the first part of the log entry
                    parts = line.split()
                    if len(parts) < 15:
                        continue  # Skip lines that don't have enough parts

                    log_date_str = parts[0]  # Adjust the index as necessary
                    log_date = datetime.strptime(log_date_str, '%Y-%m-%d')  # Parsing the date

                    # Check if the log date is within the start_date and end_date range
                    if (start_date is None or log_date >= start_date) and \
                       (end_date is None or log_date <= end_date):
                        all_entries.append(line.strip())  # Add the log line to the list
        except UnicodeDecodeError:
            # If UTF-8 fails, try with 'latin-1' encoding
            with open(file_path, 'r', encoding='latin-1') as file:
                for line in file:
                    if line.startswith("#"):
                        continue

                    parts = line.split()
                    if len(parts) < 15:
                        continue

                    log_date_str = parts[0]  # Adjust the index as necessary
                    log_date = datetime.strptime(log_date_str, '%Y-%m-%d')

                    if (start_date is None or log_date >= start_date) and \
                       (end_date is None or log_date <= end_date):
                        all_entries.append(line.strip())  # Add the log line to the list

    return all_entries

def only_get(all_entries):
  """Get only the entries that contain the word 'GET'."""
  get_entries = []

  for entry in all_entries:
    if 'GET' in entry:
      get_entries.append(entry)

  return get_entries

