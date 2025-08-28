import requests
import csv

def get_ip_info(ip_address, token=None):
    url = f"https://ipinfo.io/{ip_address}/json"
    if token:
        url += f"?token={token}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data for {ip_address}: {e}")
        return None

def main():
    input_file = 'ips2.txt'  # Replace with your text file containing IP addresses
    output_file = 'ip_geo_info2.csv'    # Output CSV file
    token = 'f32e6767c4935c'        # Optional: replace with your API token if you have one

    with open(input_file, 'r', encoding='utf-8') as file:
        ip_addresses = file.read().splitlines()

    # Open the CSV file for writing
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['IP Address', 'Location', 'City', 'Region', 'Country', 'Organization']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()  # Write the header row

        for ip in ip_addresses:
            info = get_ip_info(ip, token)
            if info:
                writer.writerow({
                    'IP Address': ip,
                    'Location': info.get('loc', 'N/A'),
                    'City': info.get('city', 'N/A'),
                    'Region': info.get('region', 'N/A'),
                    'Country': info.get('country', 'N/A'),
                    'Organization': info.get('org', 'N/A')
                })
                print(f"Data for {ip} written to CSV.")

if __name__ == "__main__":
    main()
