# Momo-Analyst

Momo-Analyst is a comprehensive tool for analyzing mobile money transactions. It provides visualizations, data categorization, and reporting features to help users gain insights into their financial data.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Data Visualization**: Interactive charts and graphs to visualize transaction data.
- **Data Categorization**: Categorizes transactions into various types such as Airtime, Bundles, CashPower, etc.
- **Reporting**: Generate and download PDF reports of transaction data.
- **Search and Filter**: Search and filter transactions based on various criteria.
- **User-Friendly Interface**: Easy-to-use interface with navigation and alerts.

## Project Architecture Overview

![Alt text](/images/Overview.png)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Bonaparte003/Momo-Analyst.git
    cd Momo-Analyst
    ```

2. Prepare your environments:
    ```sh
    ./prepare_me.sh
    ```

3. Create a .env file:
    ``` touch .env
    ```

4. In the .env include your for Database Connections
    ``` MYSQL_HOST=
        MYSQL_USER=
        MYSQL_PASSWD=
        DB=```
5. Update the create user and database credentials in prepare.sql



## Usage

1. Start the application:
    ```
    python3 api.py
    ```

2. Upload transaction files in XML format through the "Add File" section.

3. Navigate through different sections to view charts, tables, and reports.

## Demo
![Alt text](/images/1.png)
![Alt text](/images/2.png)
![Alt text](/images/3.png)
![Alt text](/images/4.png)
![Alt text](/images/5.png)
![Alt text](/images/6.png)

## API DOCUMENTATION
### Endpoints
### Base URL

#### 1. Uploading a file


##### POST /file

- this API uploads the content file of the xml, which is strictly the file format
to upload

##### GET /database_return

- Returns the Json Cleaned Data from the Database in the below format

{
    "data": {
        "airtime": [
            {
                "TxId": "12345",
                "Amount": 50.00,
                "Date": "2025-02-17",
                ...
            },
            {
                "TxId": "12346",
                "Amount": 30.00,
                "Date": "2025-02-16",
                ...
            }
        ],
        "bundles": [
            {
                "TxId": "22345",
                "Amount": 100.00,
                "Date": "2025-02-17",
                ...
            },
            {
                "TxId": "22346",
                "Amount": 200.00,
                "Date": "2025-02-16",
                ....
            }
        ],
        "cashpower": [
            {
                "Token":151513513515
                "TxId": "32345",
                "Amount": 500.00,
                "Date": "2025-02-17",
                ...
            },
            {
                "Token": 12313213
                "TxId": "32346",
                "Amount": 300.00,
                "Date": "2025-02-16",
                ...
            }
        ],
        "payments": [
            {
                "TxId": "42345",
                "Amount": 10.00,
                "Date": "2025-02-17",
                ...
            },
            {
                "TxId": "42346",
                "Amount": 5.00,
                "Date": "2025-02-16",
                ...
            }
        ]
    }
}

## REPORT SAMPLE
![Alt text](/images/report.png)