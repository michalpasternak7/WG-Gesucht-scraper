# WG-Gesucht-scraper

## Overview
This Python script is designed to scrape WG-Gesucht, a popular platform for shared housing listings, to gather information about available rooms or apartments in Berlin. The script utilizes BeautifulSoup for web scraping, pandas for data manipulation, and requests for HTTP requests.

## Usage
To use the script, you can call the get_data() function without any arguments to scrape WG-Gesucht listings for yesterday's date by default.
```python
data = get_data()
```

You can also specify a date and timeout in minutes:
data = get_data(date='dd.mm.yyyy', timeout_minutes=15)

AWS Lambda Deployment
The get_data_lambda() function is designed for deployment on AWS Lambda. It returns the scraped data as a JSON object.

To deploy this function on AWS Lambda:

Zip the script with its dependencies.
Create a new Lambda function in the AWS Management Console.
Upload the ZIP file.
Set the handler to script_name.get_data_lambda (replace script_name with your actual script's name).
Save and test the Lambda function.
