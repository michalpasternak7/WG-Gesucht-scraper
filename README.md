# WG-Gesucht-scraper

## Overview
This Python script is designed to scrape WG-Gesucht, a popular platform for shared housing listings, to gather information about available rooms or apartments in Berlin. The script utilizes BeautifulSoup for web scraping, pandas for data manipulation, and requests for HTTP requests.

## Usage
To use the script, you can call the `get_data()` function without any arguments to scrape WG-Gesucht listings for yesterday's date by default.
```python
data = get_data()
```

You can also specify a date and timeout in minutes:
```python
data = get_data(date='dd.mm.yyyy', timeout_minutes=15)
```

AWS Lambda Deployment
The `get_data_lambda()` function is designed for deployment on AWS Lambda. It returns the scraped data as a JSON object.

# TODO:
## add save wg
## explain google sheets

## AWS Lambda Deployment

To deploy the functions on AWS Lambda:

1. Install the dependencies in a folder. Navigate to the folder containing your script and run the following command to install the dependencies in a folder named `dependencies`:

```bash
pip install --target dependencies requests
```

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
    - Click on "Layers".
    - Add pandas by searching for "AWSSDKPandas-Python311".

4. Upload the ZIP file.
    - Click on "Upload from" > ".zip file" and upload your `your_lambda_function.zip`.
    - Now you should be able to see the code.

5. In Runtime settings, set the Handler to script_name.function_name (replace script_name with your actual script's name).

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