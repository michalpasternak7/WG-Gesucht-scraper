# WG-Gesucht-scraper

## Overview
This collection of Python scripts is designed to scrape WG-Gesucht, a popular platform for shared housing listings, to gather information about available rooms or apartments in Berlin. The `get_wg_list.py` script uses BeautifulSoup for web scraping, pandas for data manipulation, and requests for HTTP requests. The `save_wg_list.py` and `save_wg_list_local.py` scripts save the gathered data to a Google Spreadsheet using the gspread library.

## Scripts

### 1. get_wg_list.py
#### Overview:
This script scrapes WG-Gesucht listings and returns the data as a JSON object.

#### Dependencies:
- `requests`: For HTTP requests
- `BeautifulSoup`: For web scraping
- `pandas`: For data manipulation

#### Usage:
- To use the script, you can call the `get_data()` function without any arguments to scrape WG-Gesucht listings for yesterday's date by default.
```python
data = get_data()
```

- You can also specify a date and timeout in minutes:
```python
data = get_data(date='dd.mm.yyyy', timeout_minutes=15)
```

- The `get_data_lambda()` function is designed for deployment on AWS Lambda. It returns the scraped data as a JSON object. It's based on `get_data()` with the default values of `date=YESTERDAY, timeout_minutes=15`.

1. Deploy the script as an AWS Lambda function.


### 2.  save_wg_list.py
#### Overview:
This script is designed to be deployed on AWS Lambda and saves the event data received from `get_wg_list`'s `get_data_lambda` function to a Google Spreadsheet.

#### Dependencies:
- `gspread`: For Google Sheets API

#### Usage:
1. Ensure you have `service_account.json` in the same directory for authentication.
2. Deploy the script as an AWS Lambda function.


### 3. save_wg_list_local.py
#### Overview:
This script retrieves data using the `get_data()` function from `get_wg_list.py` and saves it to a Google Spreadsheet. This script is not meant to be deployed on AWS Lambda.

#### Dependencies:
- `json`: Standard Python library
- `gspread`: For Google Sheets API
- `get_wg_list`: Custom module to fetch data

#### Usage:
1. Ensure you have service_account.json in the same directory for authentication.
2. Run the script locally.




## Setting Up Google Sheets for [gspread](https://docs.gspread.org/en/v6.0.0/)

### Step 1: Create a New Google Cloud Project
1. Navigate to the [Google Cloud Platform](https://console.cloud.google.com/) and create a new project.

### Step 2: Create Service Account Credentials
1. Go to the **APIs & Services** tab.
2. Click on **Credentials** and then **Create Credentials**.
3. Select **Service Account**.
4. Once the Service Account credentials are created, copy the email associated with it.

### Step 3: Share Google Spreadsheet with Service Account
1. Open your Google Spreadsheet.
2. Click on **Share** in the top-right corner.
3. Paste the copied Service Account email and set its permission to **Editor** or **Owner**.

### Step 4: Generate and Download JSON Key
1. In the **Credentials** page, click on the email of the Service Account you created.
2. Navigate to the **Keys** tab and click on **Add Key**.
3. Select **JSON** as the key type. This will download a file containing all the necessary keys for your code to communicate with the Service Account.
4. Move this downloaded file into your project folder and rename it to `service_account.json`.

### Step 5: Enable Google APIs
1. Go back to the **APIs & Services** dashboard.
2. Click on **Enable APIs and Services**.
3. Search for **Google Drive API** and **Google Sheets API**.
4. Enable both APIs.




## AWS Lambda Deployment

### Step 1: Prerequisites

- Install the dependencies in a folder. Navigate to the folder containing your script and run the following command to install the dependencies in a folder named `dependencies`:

```bash
pip install --target dependencies requests
```

(**Note:** for dependencies that take up a lot of space, like pandas, it's better to not include them and add them later on from the layers.)

- Zip the script with its dependencies. You can use the following command in your terminal or command prompt:
```bash
zip -r your_lambda_function.zip your_script.py your_dependencies_folder/
```
Replace `your_script.py` with the name of your Python script and `your_dependencies_folder/` with the folder containing your dependencies.

(when you zip the dependencies you can include the `service_account.json`)

### Step 2: Create Lambda Function
- Go to [AWS Lambda Console](https://console.aws.amazon.com/lambda/).
- Click on "**Create function**".
- Choose "**Author from scratch**".
- Configure the function:
    - **Name**: Enter a name for your Lambda function.
    - **Runtime**: Choose "**Python 3.11**".
- Click on "Create function".

### Step 3: Add Pandas Layer (if necessary)
- Navigate to Layers and search for "**AWSSDKPandas-Python311**" (that's why we choose "Python 3.11" earlier).
- Add this layer to your function.

### Step 4: Upload ZIP File
- Click on "**Upload from**" > "**.zip file**" and upload your `your_lambda_function.zip`.
- Now you should be able to see the code.
- In Runtime settings, set the Handler to script_name.function_name (replace script_name with your actual script's name and function_name with the relevant function).

### Step 5: Configure Timeout & Memory
- Go to `Configuration` > `Timeout` and edit the Timeout to a suitable value, e.g., `30 seconds`.
(`get_wg_list.py` works best with `15 min`, for`save_wg_list.py` `5 min` would definitely be enough)

### Step 6: Save & Test
- Save your Lambda function settings.
- Test the function to ensure proper execution.

**For the `get_data_lambda` function:**

### Step 7: Configure Destination
Open your `get_data_lambda` function and configure a destination to trigger the `save_data_lambda` function:
- Select "**Asynchronous invocation**".
- For "On Success", choose "**Lambda function**" as the destination type.
- Select the `save_data_lambda` function from the dropdown, which is responsible for saving the data.

### Step 8: Add Trigger
- Click on "**Add trigger**" in the designer section of your Lambda function.
- Choose "**EventBridge**" from the trigger configuration options.
- Configure the trigger settings by creating a new rule or selecting an existing one.
- Save the trigger configuration.

### Step 9: Monitor Execution
- Go to "**Monitor**" in the Lambda console menu.
- Click on "**View CloudWatch logs**".
- Check the CloudWatch logs to verify if the Lambda function runs correctly and to troubleshoot any issues.
