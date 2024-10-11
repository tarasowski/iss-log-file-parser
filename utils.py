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
 

def get_ips_only(log_entries):
    """
    Extract IP addresses from log entries.

    Parameters:
        log_entries (list): A list of log entries as strings.

    Returns:
        list: A list of unique IP addresses.
    """
    ip_addresses = set()

    for entry in log_entries:
        parts = entry.split()
        if len(parts) > 8:  # Check if the entry has enough parts
            ip_address = parts[8]  # IP address is in the 9th position
            ip_addresses.add(ip_address)

    return list(ip_addresses)

def get_unique_visitors(log_entries):
    """
    Get a set of unique visitor IP addresses from the log entries.

    Args:
        log_entries (list): List of log entries to process.

    Returns:
        set: A set of unique visitor IP addresses.
    """
    unique_ips = set()  # Initialize an empty set to store unique IP addresses

    for entry in log_entries:
        # Split the log entry into parts to access the IP address
        parts = entry.split()
        if len(parts) > 5:  # Ensure there are enough parts in the log entry
            visitor_ip = parts[8]  # Assuming the visitor's IP is at index 5
            unique_ips.add(visitor_ip)  # Add the IP to the set (automatically handles duplicates)

    return unique_ips

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

