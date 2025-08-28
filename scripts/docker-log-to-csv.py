import json
import csv

# Define the input and output file paths
docker_log_file = '.\sshmitmlast.logs'  # Path to your Docker log file
output_csv_file = 'sshmitm-requests.csv'   # Path to the output CSV file

# Open the Docker log file for reading
with open(docker_log_file, 'r') as log_file:
    # Open the CSV file for writing
    with open(output_csv_file, 'w', newline='') as csv_file:
        # Define the CSV writer
        csv_writer = csv.writer(csv_file)
        
        # Write the header row to the CSV file
        csv_writer.writerow([
            'sessionid', 
            'client_ip', 
            'client_port',
            'client_version', 
            'product_name', 
            'vendor_url', 
            'tid', 
            'module', 
            'timestamp', 
            'level'
        ])
        
        # Read each line in the Docker log file
        for line in log_file:
            try:
                # Parse the JSON log entry
                data = json.loads(line)
                
                # Initialize variables for the fields
                client_ip = None
                client_port = None
                client_version = data.get('client_version', '')
                product_name = data.get('product_name', '')
                vendor_url = data.get('vendor_url', '')
                tid = data['tid']
                module = data['module']
                sessionid = data['sessionid']
                timestamp = data['timestamp']
                level = data['level']
                
                # Check if client_address exists and extract ip and port
                if 'client_address' in data:
                    client_ip = data['client_address']['ip']
                    client_port = data['client_address']['port']
                
                # If client_ip and client_port are still None, set them to empty strings
                if client_ip is None:
                    client_ip = ''
                if client_port is None:
                    client_port = ''
                
                # Write the extracted data to the CSV file
                csv_writer.writerow([
                    sessionid,
                    client_ip, 
                    client_port, 
                    client_version, 
                    product_name, 
                    vendor_url, 
                    tid, 
                    module, 
                    timestamp, 
                    level
                ])
            except json.JSONDecodeError:
                print("Error decoding JSON for line:", line)
            except KeyError as e:
                print(f"Missing key {e} in line:", line)

print(f"Data has been written to {output_csv_file}.")
