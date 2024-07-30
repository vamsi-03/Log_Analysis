import csv
import re
from datetime import datetime
import os

# Define a function to parse each log line
def parse_log_line(line):
    # Define regex patterns for different log levels
    log_pattern = r'\[(INFO|ERROR|WARN|WARNING|DEBUG|TRACE)\s*\] (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}) ([^ ]+) - (.+)'

    match = re.match(log_pattern, line)
    
    if match:
        log_level, timestamp, source, message = match.groups()
        timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S')
        return {
            'Timestamp': timestamp,
            'LogLevel': log_level,
            'Source': source,
            'Message': message,
            'ThreadID': '',
            'ErrorCode': '',
        }
    
    return None

# Function to parse the log file and write to CSV
def parse_logs_to_csv(log_folder_path, csv_file_path):
    # Initialize a list to store parsed rows
    parsed_rows = []

    # Iterate through all files in the specified folder
    for log_file in os.listdir(log_folder_path):
        if log_file.startswith('build_'):
            # Read the log file
            with open(os.path.join(log_folder_path, log_file), 'r') as logfile:
                lines = logfile.readlines()

            # Parse each line
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
log_folder_path = 'BuildFiles'  # Folder containing the log files
csv_file_path = 'parsed_log.csv'

# Call the function to parse logs and write to CSV
parse_logs_to_csv(log_folder_path, csv_file_path)
