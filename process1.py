import pandas as pd
from datetime import timedelta
import os
import argparse

def extract_trips(input_path, output_dir):
    # Load Parquet file into DataFrame
    df = pd.read_parquet(input_path)

    # Convert 'timestamp' column to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Sort DataFrame by unit and timestamp
    df.sort_values(by=['unit', 'timestamp'], inplace=True)

    # Initialize variables for trip detection
    current_unit = None
    trip_number = 0

    # Iterate through DataFrame to extract trips
    for unit, unit_data in df.groupby('unit'):
        current_unit = unit
        trip_number = 0

        for idx, row in unit_data.iterrows():
            if idx > 0 and (row['timestamp'] - unit_data.at[idx - 1, 'timestamp']).total_seconds() > timedelta(hours=7).total_seconds():

                # Start a new trip
                trip_number = 0

            # Create CSV file for the current trip
            trip_filename = f"{current_unit}_{trip_number}.csv"
            trip_path = os.path.join(output_dir, trip_filename)

            # Save trip data to CSV
            trip_data = row[['latitude', 'longitude', 'timestamp']]
            trip_data.to_csv(trip_path, index=False, mode='a' if os.path.exists(trip_path) else 'w')

            # Increment trip number
            trip_number += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract trips from GPS data")
    parser.add_argument("--to_process", required=True, help="Path to the Parquet file to be processed")
    parser.add_argument("--output_dir", required=True, help="The folder to store resulting CSV files")
    args = parser.parse_args()

    # Call the function to extract trips
    extract_trips(args.to_process, args.output_dir)
