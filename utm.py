from datetime import datetime

# UTM parameters to filter
utm_parameters = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content']

# Function to check if a query string contains any UTM parameters
def contains_utm(query):
    if query == "-":  # No query string present
        return False
    return any(param in query for param in utm_parameters)

# Function to process the log entries with date filtering and sorting
def analyze_logs(log_entries, start_date=None, end_date=None):
    # List to store log entries containing UTM queries
    found_entries = []

    for line in log_entries:
        # Skip comment lines starting with '#'
        if line.startswith("#"):
            continue

        # Split the log line by space
        parts = line.split()

        # Ensure the log line has the expected number of fields
        if len(parts) >= 15:  # Adjust this based on the expected log format
            log_date_str = parts[0]  # Assuming date is the first field
            cs_uri_query = parts[5]  # Assuming the cs-uri-query is at index 5

            # Parse the date from the log entry
            log_date = datetime.strptime(log_date_str, '%Y-%m-%d')  # Adjust format if necessary

            # Check date filtering
            if start_date and log_date < start_date:
                continue
            if end_date and log_date > end_date:
                continue

            # Check if the query string contains UTM parameters
            if contains_utm(cs_uri_query):
                found_entries.append((log_date, line.strip()))  # Store the log date with the log line

    # Sort entries by date
    found_entries.sort(key=lambda entry: entry[0])  # Sort by the date part of the tuple

    return [entry[1] for entry in found_entries]  # Return the list of found log entries

