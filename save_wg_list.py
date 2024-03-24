# Imports
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from get_wg_list import get_data
from datetime import datetime, timedelta

# Helper function
def count_filled_rows(worksheet):
    # Get the values in the worksheet
    values = worksheet.get_all_values()
    
    # Check if the sheet is empty
    if not values:
        return 0  # Return 0 if the sheet is empty
    
    # Count the number of non-empty rows
    num_rows_filled = sum(1 for row in values if any(row))
    
    return num_rows_filled

# Get the data from WG-Gesucht
yesterday = (datetime.now().date() - timedelta(days=1)).strftime('%d.%m.%Y')
append_df = get_data(date=yesterday, timeout_minutes=30)

# Connect to Google Spreadsheet
# Authenticate and connect to Google Sheets
gc = gspread.service_account(filename="./service_account.json")

# Open the Google Sheets document
worksheet = gc.open("wg-gesucht_list").worksheet("list_data")

# Append data to Google Spreadsheet
set_with_dataframe(worksheet, append_df, row=count_filled_rows(worksheet)+1, include_index=False, include_column_header=False)