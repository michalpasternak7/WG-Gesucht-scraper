# Imports
import json
import gspread
from get_wg_list import get_data


def save_data(data_df):
    """Saves the wg-list data to a Google Spreadsheet."""

    # Convert df to list of lists
    data_list = data_df.values.tolist()

    # Connect to Google Spreadsheet
    # Authenticate and connect to Google Sheets
    gc = gspread.service_account(filename="./service_account.json")

    # Open the Google Sheets document
    worksheet = gc.open("wg-gesucht_list").worksheet("list_data")

    # Append data to Google Spreadsheet
    worksheet.append_rows(data_list, value_input_option='RAW')
    
    print("Data appended successfully.")


# Get the data from WG-Gesucht
data_df = get_data()

# Save the data to Google Spreadsheet
save_data(data_df) 