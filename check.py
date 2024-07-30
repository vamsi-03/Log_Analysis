import csv
import re
from datetime import datetime

# Define a function to parse each log line
def parse_log_line(line):
    # Define regex patterns for INFO log level
    info_log_pattern = r'\[WARNING\s*\] (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) ([^ ]+) - (.+)'

    info_match = re.match(info_log_pattern, line)
    
    if info_match:
        timestamp, source, message = info_match.groups()
        timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S')
        return {
            'Timestamp': timestamp,
            'LogLevel': 'INFO',
            'Source': source,
            'Message': message,
            'ThreadID': '',
            'ErrorCode': '',
        }
    
    return None

# Function to parse the log file and write to CSV
def parse_log_to_csv(log_file_path, csv_file_path):
    # Read the log file
    with open(log_file_path, 'r') as logfile:
        lines = logfile.readlines()

    # Parse each line
    parsed_rows = []
    for line in lines:
        parsed_line = parse_log_line(line.strip())
        if parsed_line:
            parsed_rows.append(parsed_line)

    # Define the CSV header
    header = ['Timestamp', 'LogLevel', 'Source', 'Message', 'ThreadID', 'ErrorCode']

    # Write the parsed data into a CSV file
    with open(csv_file_path, 'w', newline='') as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=header)
        csvwriter.writeheader()
        csvwriter.writerows(parsed_rows)

# Define file paths
log_file_path = r'D:\AIML_WS\Log_Analysis\BuildFiles\build_1.log'  # Replace with your log file path
csv_file_path = 'parsed1_log.csv'

# Call the function to parse log and write to CSV
parse_log_to_csv(log_file_path, csv_file_path)
