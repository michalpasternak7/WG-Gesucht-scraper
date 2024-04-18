# WG-Gesucht-scraper

## Overview
This Python script is designed to scrape WG-Gesucht, a popular platform for shared housing listings, to gather information about available rooms or apartments in Berlin. The script utilizes BeautifulSoup for web scraping, pandas for data manipulation, and requests for HTTP requests.

## Usage
To use the script, you can call the '**get_data()**' function without any arguments to scrape WG-Gesucht listings for yesterday's date by default.
```python
data = get_data()
```

You can also specify a date and timeout in minutes:
```python
data = get_data(date='dd.mm.yyyy', timeout_minutes=15)
```

AWS Lambda Deployment
The '**get_data_lambda()**' function is designed for deployment on AWS Lambda. It returns the scraped data as a JSON object.

To deploy this function on AWS Lambda:

1. Zip the script with its dependencies. You can use the following command in your terminal or command prompt:
```bash
zip -r your_lambda_function.zip your_script.py your_dependencies_folder/
```
Replace your_script.py with the name of your Python script and your_dependencies_folder/ with the folder containing your dependencies.

2. Create a new Lambda function in the AWS Management Console.
3. Upload the ZIP file.
4. Set the handler to get_wg_list.get_data_lambda.
5. Save and test the Lambda function.
