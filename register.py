from load import load_all_logs, only_get
from utm import analyze_logs
from datetime import datetime
from utils import count_unique_visitors, get_ips_only, get_unique_visitors, get_entries_by_ip

logs_folder = 'logs'

start_date = datetime.strptime('2024-09-09', '%Y-%m-%d')  # Example start date
end_date = datetime.strptime('2024-09-16', '%Y-%m-%d')    # Example end date

all_get_requests = only_get(load_all_logs(logs_folder, start_date, end_date))
visits_all_with_registration = [log for log in all_get_requests if 'GET /Registrieren' in log]
visits_all_from_facebook = [log for log in all_get_requests if 'utm_source=meta' in log]
ips_all_visitors = get_ips_only(all_get_requests)
ips_of_registration_visitors = get_ips_only(visits_all_with_registration)
ips_of_facebook_visitors = get_ips_only(visits_all_from_facebook)

print(f"All unique IPs: {len(ips_all_visitors)}")
print(f"All unique IPs visited /Registrieren: {len(ips_of_registration_visitors)}")
print(f"All unique IPs coming from facebook: {len(ips_of_facebook_visitors)}")


# check each ip from facebook if it visited the registration page

def check_facebook_ips_registration(visits_all_with_registration, ips_of_facebook_visitors):
    """
    Check if each IP from Facebook has visited the registration page.

    Args:
        visits_all_with_registration (list): List of log entries for the registration page.
        ips_of_facebook_visitors (set): Set of unique IPs from Facebook.

    Returns:
        dict: A dictionary with IP addresses as keys and a boolean indicating
              whether they visited the registration page as values.
    """
    # Initialize a dictionary to store IPs and their visit status
    ip_visit_status = {ip: False for ip in ips_of_facebook_visitors}

    # Create a set of IPs that have visited the registration page for quick lookup
    registration_ips = set()

    # Iterate through visits to the registration page and record the IPs
    for entry in visits_all_with_registration:
        parts = entry.split()
        if len(parts) > 5:  # Ensuring there are sufficient parts
            registration_ips.add(parts[8])  # Assuming index 8 is the IP address

    # Check each Facebook IP against the registration IPs
    for ip in ips_of_facebook_visitors:
        if ip in registration_ips:
            ip_visit_status[ip] = True  # Mark as visited if found

    return ip_visit_status


facebook_ip_visits = check_facebook_ips_registration(visits_all_with_registration, ips_of_facebook_visitors)

print(f"IPs from Facebook that visited the registration page: {sum(facebook_ip_visits.values())}")

# display the ips that visited the registration page
for ip, visited in facebook_ip_visits.items():
    if visited:
      print(f"This ip has visited the /Registration: {ip}")


t = get_entries_by_ip(visits_all_from_facebook, '212.211.197.10')

print(t)
exit()

