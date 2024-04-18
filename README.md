# WG-Gesucht-scraper

## Overview
This collection of Python scripts is designed to scrape WG-Gesucht, a popular platform for shared housing listings, to gather information about available rooms or apartments in Berlin. The `get_wg_list.py` script uses BeautifulSoup for web scraping, pandas for data manipulation, and requests for HTTP requests. The `save_wg_list.py` and `save_wg_list_local.py` scripts save the gathered data to a Google Spreadsheet using the gspread library.


## get_wg_list.py
### Overview:
This script scrapes WG-Gesucht listings and returns the data as a JSON object.

### Dependencies:
- `requests`: For HTTP requests
- `BeautifulSoup`: For web scraping
- `pandas`: For data manipulation

### Usage:
- To use the script, you can call the `get_data()` function without any arguments to scrape WG-Gesucht listings for yesterday's date by default.
```python
data = get_data()
```

- You can also specify a date and timeout in minutes:
```python
data = get_data(date='dd.mm.yyyy', timeout_minutes=15)
```

- The `get_data_lambda()` function is designed for deployment on AWS Lambda. It returns the scraped data as a JSON object. It's based on `get_data()` with the default values of `date=YESTERDAY, timeout_minutes=15`.



## save_wg_list.py
### Overview:
This script is designed to be deployed on AWS Lambda and saves the event data received from `get_wg_list`'s `get_data_lambda` function to a Google Spreadsheet.

### Dependencies:
- `gspread`: For Google Sheets API

### Usage:
- Ensure you have `service_account.json` in the same directory for authentication.
- Deploy the script as an AWS Lambda function.


## save_wg_list_local.py
### Overview:
This script retrieves data using the `get_data()` function from `get_wg_list.py` and saves it to a Google Spreadsheet. This script is not meant to be deployed on AWS Lambda.

### Dependencies:
- `json`: Standard Python library
- `gspread`: For Google Sheets API
- `get_wg_list`: Custom module to fetch data

### Usage:
- Ensure you have service_account.json in the same directory for authentication.
- Run the script locally.


# TODO:
## explain google sheets

## AWS Lambda Deployment

To deploy the functions on AWS Lambda:

1. Install the dependencies in a folder. Navigate to the folder containing your script and run the following command to install the dependencies in a folder named `dependencies`:

```bash
pip install --target dependencies requests
```

(**Note:** for dependencies that take up a lot of space, like pandas, it's better to not include them and add them later on from the layers.)

2. Zip the script with its dependencies. You can use the following command in your terminal or command prompt:
```bash
zip -r your_lambda_function.zip your_script.py your_dependencies_folder/
```
Replace `your_script.py` with the name of your Python script and `your_dependencies_folder/` with the folder containing your dependencies.

(when you zip the dependencies you can include the `service_account.json`)

3. Create a new Lambda function in the AWS Management Console.
    - Go to [AWS Lambda Console](https://console.aws.amazon.com/lambda/).
    - Click on "Create function".
    - Choose "Author from scratch".
    - Configure the function:
        - **Name**: Enter a name for your Lambda function.
        - **Runtime**: Choose "Python 3.11".
    - Click on "Create function".

4. Add Pandas Layer (if necessary)
    - Click on "Layers".
    - Add pandas by searching for "AWSSDKPandas-Python311" (that's why we choose "Python 3.11" earlier).

4. Upload the ZIP file.
    - Click on "Upload from" > ".zip file" and upload your `your_lambda_function.zip`.
    - Now you should be able to see the code.

5. In Runtime settings, set the Handler to script_name.function_name (replace script_name with your actual script's name and function_name with the relevant function).

6. Go to `Configuration` > `Timeout` and edit the Timeout to a suitable value, e.g., `30 seconds`.
    (`get_wg_list.py` works best with `15 min`, for`save_wg_list.py` `5 min` would definitely be enough)

7. Save and test the Lambda function.

For the `get_data_lambda` function:

8. Open your `get_data_lambda` function and configure a destination to trigger the `save_data_lambda` function:
    - Select "Asynchronous invocation".
    - For "On Success", choose "Lambda function" as the destination type.
    - Select the `save_data_lambda` function from the dropdown, which is responsible for saving the data.

9. Add a trigger to your Lambda function:
    - Click on "Add trigger" in the designer section of your Lambda function.
    - Choose "EventBridge" from the trigger configuration options.
    - Configure the trigger settings by creating a new rule or selecting an existing one.
    - Save the trigger configuration.

10. Monitor your Lambda function's execution:
    - Go to "Monitor" in the Lambda console menu.
    - Click on "View CloudWatch logs".
    - Check the CloudWatch logs to verify if the Lambda function runs correctly and to troubleshoot any issues.