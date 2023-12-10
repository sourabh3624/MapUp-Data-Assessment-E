# process2.py

import requests
import os
import argparse
from dotenv import load_dotenv

def upload_to_tollguru(input_folder, output_dir):
    # Load environment variables
    load_dotenv()

    # API configuration
    api_url = os.getenv("TOLLGURU_API_URL")
    api_key = os.getenv("TOLLGURU_API_KEY")

    # Iterate through CSV files in the input folder
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".csv"):
            # Create full file path
            file_path = os.path.join(input_folder, file_name)

            # Prepare headers and payload
            headers = {'x-api-key': api_key, 'Content-Type': 'text/csv'}
            payload = {'vehicleType': '5AxlesTruck', 'mapProvider': 'osrm'}

            # Send request to TollGuru API
            with open(file_path, 'rb') as file:
                response = requests.post(f'{api_url}/gps-tracks-csv-upload', params=payload, data=file, headers=headers)

            # Save JSON response to the output directory
            json_response_path = os.path.join(output_dir, f"{file_name.replace('.csv', '.json')}")
            with open(json_response_path, 'w') as json_file:
                json_file.write(response.text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload GPS tracks to TollGuru API")
    parser.add_argument("--to_process", required=True, help="Path to the CSV folder")
    parser.add_argument("--output_dir", required=True, help="Folder to store resulting JSON files")
    args = parser.parse_args()

    # Call the function to upload to TollGuru API
    upload_to_tollguru(args.to_process, args.output_dir)
