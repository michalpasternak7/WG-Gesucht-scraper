# Imports
import gspread

def save_data_lambda(event, context):
    """Saves the data it get's from get_wg_list to a Google Spreadsheet."""

    # Transform the output of get_wg_list to something we can feed into the Google Spreadsheet
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
    
    print("Data appended successfully.")
    
    