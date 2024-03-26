# Imports
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
import random
from datetime import datetime, timedelta
import json

# Constants
YESTERDAY = (datetime.now().date() - timedelta(days=1)).strftime('%d.%m.%Y')
#TODAY = datetime.now().date().strftime('%d.%m.%Y')
LAST_PAGE = 1000

# Regex patterns 
date_pattern = r'\b\d{2}\.\d{2}\.\d{4}\b'
numbers_pattern = r'\d+'

#Functions
def get_size_and_gender(row):
    try:
        size_and_genders = row[1].a.span.get('title')
        return size_and_genders
    except:
        return ''

def get_entry_date(row):
    try:
        dates = re.search(date_pattern, row[2].a.span.text)
        return dates[0]
    except:
        return ''
    
def get_price(row):
    try:
        price = int(re.search(numbers_pattern, row[3].span.b.text).group(0))
        return price
    except:
        return -1

def get_sqr_m(row):
    try:
        sqr_m = int(re.search(numbers_pattern, row[4].a.span.text).group(0))
        return sqr_m
    except:
        return -1
    
def get_city_part(row):
    try:
        text = row[5].a.span.text.replace('\n', '').replace(' ', '')
        city_part = text[0] + ''.join([' ' + char if char.isupper() and text[i - 1].islower() else char for i, char in enumerate(text)][1:])
        return city_part
    except:
        return ''
    
def get_available_from(row):
    try:
        available_from = row[6].span.text
        return available_from
    except:
        return ''

def get_available_to(row):
    try:
        available_to = row[7].span.text
        return available_to
    except:
        return ''

def get_wg_list_data(row):
    """Extract data from a single offer."""
    wg_list_data = dict()

    # if the row has a href
    try:
        href = row[1].a.get('href')

        # get the wg_id out of the href
        if href.endswith('html'):
            wg_id = href.split('.')[-2]
            wg_list_data['wg_id'] = wg_id
        else:
            wg_list_data['wg_id'] = None
        
        wg_list_data['href'] = href

        size_and_genders = get_size_and_gender(row)
        wg_list_data['size_and_genders'] = size_and_genders

        entry_date = get_entry_date(row)
        wg_list_data['entry_date'] = entry_date

        price = get_price(row)
        wg_list_data['price'] = price

        sqr_m = get_sqr_m(row)
        wg_list_data['sqr_m'] = sqr_m

        city_part = get_city_part(row)
        wg_list_data['city_part'] = city_part

        available_from = get_available_from(row)
        wg_list_data['available_from'] = available_from

        available_to = get_available_to(row)
        wg_list_data['available_to'] = available_to

        return wg_list_data

    except:
        return None

def get_wg_list_from_url(url):
    """Scrape data from a given URL."""
    try:
        # Open one site and get all offers from it
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        wg_list = soup.find("table", class_="table table-condensed")

        # Get all rows with wg offers
        wg_offers = wg_list.tbody.find_all('tr')
        offers_list = [get_wg_list_data(offer.find_all('td')) for offer in wg_offers]
        return pd.DataFrame(offers_list)
    
    except requests.RequestException as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}][{url}] An error occurred: {e}")
        return None
    
    except Exception as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}][{url}] An exception occurred: {e}")
        print(r.url)
        return None

def try_scraping(url, max_retries=3, initial_delay=90):
    """Try to scrape the data, but only a few times, to avoid running too long.
    In case there is a problem with getting the data, it's probably because of the captcha,
    so there is a delay implemented to wait it out."""

    retries = 0
    delay = initial_delay
    while retries < max_retries:

        # Take a break to not trigger the captcha too quick
        time.sleep(random.uniform(2, 10))

        # Open one site and get all offers from it
        data_to_append = get_wg_list_from_url(url)

        # We got data
        if data_to_append is not None:
            return data_to_append
        
        # If there was a problem while getting the data from the website
        retries += 1
        if retries < max_retries:
            # Take a longer break, because the captcha probably appeared
            random_delay = random.uniform(delay, delay + 60)
            print(f"Retrying in {random_delay} seconds...")
            time.sleep(random_delay)
            delay += 30
     
    return None

# Scraping all sites
def get_data(date=YESTERDAY, timeout_minutes=15):
    """Get all WG-Gesucht listings for a certain date."""

    start_time = datetime.now()

    columns = ['wg_id', 'href', 'size_and_genders', 'entry_date', 'price', 'sqr_m', 'city_part', 'available_from', 'available_to']
    existing_data = pd.DataFrame(columns=columns)

    date_reached = False # Checks if we have reached the date we want data for (since we start scraping when that date has passed and want to skip the new listings for now)
    
    for i in range(0, LAST_PAGE): # This is like an infinite while loop, but it's easier to have a counter in a for loop  

        # Check if the timeout has been exceeded
        elapsed_time = datetime.now() - start_time
        if elapsed_time > timedelta(minutes=timeout_minutes):
            print("Timeout reached. Exiting function.")
            break      

        # Generate url
        url = f'https://www.wg-gesucht.de/wg-zimmer-in-Berlin.8.0.0.{i}.html'
        data_to_append = try_scraping(url)

        # if scraping a site failed
        if data_to_append is None:
            print(f"{datetime.now().strftime('%H:%M:%S')}][{url}] Could not be scraped.")
            continue

        else:
            # if the scraping was succesfull
            # Drop rows with NaN values in 'wg_id' column
            data_to_append.dropna(subset=['wg_id'], inplace=True, ignore_index=True)

            # If there is no new data left, end looping
            if not (data_to_append['entry_date'] == date).any() and date_reached:
                print(f"[{datetime.now().strftime('%H:%M:%S')}][{i}] End of data for: {date}")
                break
            
            # Compare new data to existing data
            # If any of the data is not in the existing_data yet
            if not data_to_append['href'].isin(existing_data['href']).all():

                # Don't include data that's already in the existing_data df.
                # This can happen, because the scraping takes time and new listings can be added while it runs.
                new_rows = data_to_append[~data_to_append['href'].isin(existing_data['href'])]

                # Only take listings from desired date
                new_rows = new_rows[new_rows['entry_date'] == date]

                # If we hit the desired date
                if new_rows.shape[0] > 0:
                    date_reached = True
                
                # The data is from the desired date so we append it.
                if date_reached:
                    # Append data to the existing_data DataFrame
                    existing_data = pd.concat([existing_data, new_rows], ignore_index=True)
                    print(f"[{datetime.now().strftime('%H:%M:%S')}][{url}] {new_rows.shape[0]} new WG's appended successfully.")

                # We are not at the desired date yet
                else:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}][{url}] {date} not reached yet.")

            # There is no more WG's to append
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}][{url}] No WG's to appended.")

    return existing_data

def get_data_lambda(event, context):
    """Lambda function to be able to run this on AWS Lambda.
    Does the same as get_data(), but the output is turned into a JSON (not a JSON string)."""
    data_df = get_data()
    data_json = data_df.to_json(orient='records')
    data_json = json.loads(data_json)
    print(data_json)
    print(f"Returned json based on df of shape:{data_df.shape}")
    return data_json