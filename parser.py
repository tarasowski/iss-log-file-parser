import os
from datetime import datetime

# Path to the logs folder
logs_folder = './logs'

# UTM parameters to filter
utm_parameters = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content']

# Function to check if a query string contains any UTM parameters
def contains_utm(query):
    if query == "-":  # No query string present
        return False
    return any(param in query for param in utm_parameters)

# Function to process the log files with date filtering and sorting
def analyze_logs(logs_folder, start_date=None, end_date=None):
    # List to store log entries containing UTM queries
    found_entries = []
    
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
                    
                    # Split the log line by space
                    parts = line.split()
                    
                    # Ensure the log line has the expected number of fields
                    if len(parts) >= 15:
                        # Assuming the date is in the first field and in a standard format (e.g., "YYYY-MM-DD")
                        log_date_str = parts[0]  # Adjust index as needed based on your log format
                        cs_uri_query = parts[5]   # The cs-uri-query field
                        
                        # Parse the date from the log entry
                        log_date = datetime.strptime(log_date_str, '%Y-%m-%d')  # Adjust format if necessary
                        
                        # Check date filtering if start_date and end_date are provided
                        if start_date and log_date < start_date:
                            continue
                        if end_date and log_date > end_date:
                            continue
                        
                        # Check if the query string contains UTM parameters
                        if contains_utm(cs_uri_query):
                            found_entries.append((log_date, line.strip()))  # Store the log date with the log line
    
        except UnicodeDecodeError:
            # If UTF-8 fails, try with 'latin-1'
            with open(file_path, 'r', encoding='latin-1') as file:
                for line in file:
                    # Skip comment lines starting with '#'
                    if line.startswith("#"):
                        continue
                    
                    # Split the log line by space
                    parts = line.split()
                    
                    # Ensure the log line has the expected number of fields
                    if len(parts) >= 15:
                        log_date_str = parts[0]  # Adjust index as needed based on your log format
                        cs_uri_query = parts[5]   # The cs-uri-query field
                        
                        # Parse the date from the log entry
                        log_date = datetime.strptime(log_date_str, '%Y-%m-%d')  # Adjust format if necessary
                        
                        # Check date filtering if start_date and end_date are provided
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

# Define your date range for filtering
start_date = datetime.strptime('2024-09-9', '%Y-%m-%d')  # Example start date
end_date = datetime.strptime('2024-09-16', '%Y-%m-%d')    # Example end date

# Run the log analysis
utm_entries = analyze_logs(logs_folder, start_date, end_date)


# New function to process the log entries
def process_log_entries(log_entries):
    print("Processing Log Entries:")
    for entry in log_entries:
        # Check if the entry contains 'facebook' in the referrer part
        if 'facebook' in entry:
            print(entry) 

facebook_entries = [entry for entry in utm_entries if 'facebook' in entry]

print("\nFacebook Entries:")
for entry in facebook_entries:
    print(entry)


from collections import Counter

def count_unique_visitors(log_entries):
    """
    Count unique visitors by user IP address from log entries.

    Parameters:
        log_entries (list): A list of log entries as strings.

    Returns:
        dict: A dictionary with user IP addresses as keys and their visit counts as values.
        int: The total number of unique visitors.
    """
    # Counter to store unique user IP counts
    user_ip_counter = Counter()

    # Process each log entry
    for entry in log_entries:
        parts = entry.split()
        if len(parts) > 8:  # Check if the entry has enough parts
            user_ip_address = parts[8]  # User IP is in the 9th position
            user_ip_counter[user_ip_address] += 1

    # Return counts and total unique visitors
    unique_visitors = len(user_ip_counter)
    return dict(user_ip_counter), unique_visitors  

# Count unique visitors from the Facebook entries  
facebook_ip_counts, facebook_unique_visitors = count_unique_visitors(facebook_entries)

"""
print("\nUnique Visitors from Facebook:")
print("Total Unique Visitors:", facebook_unique_visitors)
print("IP Address Counts:")
print(facebook_ip_counts)
"""

from collections import defaultdict


from collections import defaultdict

def count_unique_visitors_with_details(log_entries):
    """
    Count unique visitors by user IP address from log entries and gather their details.

    Parameters:
        log_entries (list): A list of log entries as strings.

    Returns:
        dict: A dictionary with user IP addresses as keys and details about their visits as values.
        int: The total number of unique visitors.
    """
    # Dictionary to store visitor details
    visitor_details = defaultdict(lambda: {
        'count': 0,
        'methods': set(),
        'sites': set(),
        'status_codes': set()
    })

    # Process each log entry
    for entry in log_entries:
        parts = entry.split()
        if len(parts) > 11:  # Ensure we have enough parts to avoid IndexError
            user_ip_address = parts[8]  # User IP is in the 9th position
            http_method = parts[5]       # HTTP method is in the 6th position
            requested_site = parts[6]    # Requested site (URI) is in the 7th position
            status_code = parts[11]       # Status code is in the 12th position

            # Update visitor details
            visitor_details[user_ip_address]['count'] += 1
            visitor_details[user_ip_address]['methods'].add(http_method)
            visitor_details[user_ip_address]['sites'].add(requested_site)
            visitor_details[user_ip_address]['status_codes'].add(status_code)

    # Return counts and total unique visitors
    unique_visitors = len(visitor_details)
    return visitor_details, unique_visitors

# Call the function
visitor_details, total_unique_visitors = count_unique_visitors_with_details(facebook_entries)

# Display the results
print("Unique Visitors Details:")
for ip, details in visitor_details.items():
    print(f"User IP: {ip}, Count: {details['count']}, HTTP Methods: {', '.join(details['methods'])}, Requested Sites: {', '.join(details['sites'])}, Status Codes: {', '.join(details['status_codes'])}")

print(f"\nTotal Unique Visitors: {total_unique_visitors}")


def get_entries_by_ip(log_entries, ip_address):
    """
    Retrieve all log entries for a specific IP address.

    Parameters:
        log_entries (list): A list of log entries as strings.
        ip_address (str): The IP address to filter the log entries.

    Returns:
        list: A list of log entries corresponding to the given IP address.
    """
    # List to store the filtered entries
    filtered_entries = []

    # Process each log entry
    for entry in log_entries:
        parts = entry.split()
        if len(parts) > 8:  # Ensure there are enough parts to access the IP address
            user_ip = parts[8]  # User IP is in the 9th position
            if user_ip == ip_address:
                filtered_entries.append(entry)

    return filtered_entries

by_ip = get_entries_by_ip(facebook_entries, '77.2.202.129')

for entry in by_ip:
    print(entry, '\n')
