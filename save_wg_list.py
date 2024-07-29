# Imports
import gspread
import boto3
import csv
import os
import io

# Set up S3 client
s3_client = boto3.client('s3')

# S3 bucket and file name from environment variables
S3_BUCKET = os.environ['S3_BUCKET']
S3_FILE_NAME = os.environ['S3_FILE_NAME']

def read_existing_csv():
    try:
        s3_object = s3_client.get_object(Bucket=S3_BUCKET, Key=S3_FILE_NAME)
        csv_content = s3_object['Body'].read().decode('utf-8')
        existing_data = list(csv.reader(io.StringIO(csv_content)))
        return existing_data
    except s3_client.exceptions.NoSuchKey:
        return []  # If the file does not exist, return an empty list

def save_data_to_s3(append_list):
    # Read existing data from S3
    existing_data = read_existing_csv()
    
    # Append new data to existing data
    combined_data = existing_data + append_list

    # Create a temporary file
    temp_file = '/tmp/temp_data.csv'
    
    # Write combined data to the temporary CSV file
    with open(temp_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        if not existing_data:  # Write header if the file was empty
            writer.writerow(['wg_id', 'href', 'size_and_genders', 'entry_date', 'price', 'sqr_m', 'city_part', 'available_from', 'available_to'])
        writer.writerows(combined_data)
    
    # Upload the CSV file to S3
    s3_client.upload_file(temp_file, S3_BUCKET, S3_FILE_NAME)
    
    # Remove the temporary file
    os.remove(temp_file)

def save_data_lambda(event, context):
    append_list = []
    for i in event['responsePayload']:
        append_list.append([i['wg_id'],
                            i['href'],
                            i['size_and_genders'],
                            i['entry_date'],
                            i['price'],
                            i['sqr_m'],
                            i['city_part'],
                            i['available_from'],
                            i['available_to']
                            ])

    # Connect to Google Spreadsheet
    # Authenticate and connect to Google Sheets
    gc = gspread.service_account(filename="./service_account.json")

    # Open the Google Sheets document
    worksheet = gc.open("wg-gesucht_list").worksheet("list_data")

    # Append data to Google Spreadsheet
    worksheet.append_rows(append_list, value_input_option='RAW')
    
    print("Data appended successfully to GS.")
    
        # Save data to S3
    save_data_to_s3(append_list)
    
    print("Data appended successfully to S3.")
