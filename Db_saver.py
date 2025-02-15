#!/usr/bin/env python3
import MySQLdb
import json
from dotenv import load_dotenv
import os
import datetime
import re

load_dotenv()

conn = MySQLdb.connect(
    host=os.getenv('MYSQL_HOST'),
    user=os.getenv('MYSQL_USER'),
    passwd=os.getenv('MYSQL_PASSWD'),
    db=os.getenv('DB')
)
cursor = conn.cursor()

sqlstatements = [
    """CREATE TABLE IF NOT EXISTS airtime (
    TxId VARCHAR(250) PRIMARY KEY NOT NULL,
    Amount INT, 
    CURRENCY VARCHAR(3),
    Date DATE,
    TIME TIME, 
    Type VARCHAR(250), 
    Balance INT, 
    Fee INT
    );""",
    
    """CREATE TABLE IF NOT EXISTS bundles(
    TxId VARCHAR(250) PRIMARY KEY NOT NULL,
    Amount INT,
    CURRENCY VARCHAR(3),
    Date DATE,
    TIME TIME,
    Type VARCHAR(250),
    Balance INT,
    Fee INT
    );
    """,
    
    """CREATE TABLE IF NOT EXISTS cashpower(
    TxId VARCHAR(250) PRIMARY KEY NOT NULL,
    TOKEN VARCHAR(250),
    Amount INT,
    CURRENCY VARCHAR(3),
    Date DATE,
    TIME TIME,
    Type VARCHAR(250),
    Balance INT,
    Fee INT
    );""",

    """CREATE TABLE IF NOT EXISTS payments(
    TxId VARCHAR(250) PRIMARY KEY NOT NULL,
    RECEIVER VARCHAR(250),
    AMOUNT INT,
    CURRENCY VARCHAR(3),
    Date DATE,
    TIME TIME,
    Type VARCHAR(250),
    Balance INT,
    Fee INT
    );""",

    """CREATE TABLE IF NOT EXISTS reversedtransactions(
    RECEIVER VARCHAR(250),
    AMOUNT INT,
    CURRENCY VARCHAR(3),
    Date DATE,
    TIME TIME,
    Type VARCHAR(250),
    BALANCE INT,
    PHONE_NUMBER VARCHAR(250),
    FEE INT
    );""",

    """CREATE TABLE IF NOT EXISTS failedtransactions(
    RECEIVER VARCHAR(250),
    AMOUNT INT,
    CURRENCY VARCHAR(3),
    Date DATE,
    TIME TIME,
    Type TEXT,
    FEE INT
    );""",

    """CREATE TABLE IF NOT EXISTS thirdparty(
    SENDER VARCHAR(250),
    AMOUNT INT,
    CURRENCY VARCHAR(3),
    Date DATE,
    TIME TIME,
    Type VARCHAR(250),
    Balance INT,
    Fee INT
    );""",

    """CREATE TABLE IF NOT EXISTS withdraw(
    AGENT VARCHAR(250),
    AMOUNT INT,
    CURRENCY VARCHAR(3),
    Date DATE,
    TIME TIME,
    Type VARCHAR(250),
    Balance INT,
    Fee INT
    );""",

    """CREATE TABLE IF NOT EXISTS nontransaction(
    NUMBER INT);""",

    """CREATE TABLE IF NOT EXISTS incomingmoney(
    SENDER VARCHAR(250),
    AMOUNT INT,
    CURRENCY VARCHAR(3),
    Date DATE,
    TIME TIME,
    Type VARCHAR(250),
    Balance INT,
    Fee INT
    );""",
    
    
    """CREATE TABLE IF NOT EXISTS transfer(
    RECEIVER VARCHAR(250),
    PHONE_NUMBER VARCHAR(250),
    AMOUNT INT,
    CURRENCY VARCHAR(3),
    Date DATE,
    TIME TIME,
    Type VARCHAR(250),
    Balance INT,
    Fee INT
    );""",

    """CREATE TABLE IF NOT EXISTS deposit(
    AMOUNT INT,
    CURRENCY VARCHAR(3),
    Date DATE,
    TIME TIME,
    Type VARCHAR(250),
    Balance INT,
    Fee INT
    );""",

    """CREATE TABLE IF NOT EXISTS codeholders(
    RECEIVER VARCHAR(250),
    CODE INT,
    TxId VARCHAR(250) PRIMARY KEY NOT NULL,
    AMOUNT INT,
    CURRENCY VARCHAR(3),
    Date DATE,
    TIME TIME,
    Type VARCHAR(250),
    Balance INT,
    Fee INT
    );"""
    
]

for statement in sqlstatements:
    cursor.execute(statement)
conn.commit()

json_files = [
    'Data_Categorization/Cleaned_Data/cleaned_Airtime.json',
    'Data_Categorization/Cleaned_Data/cleaned_Bundles.json',
    'Data_Categorization/Cleaned_Data/cleaned_cash_power.json',
    'Data_Categorization/Cleaned_Data/cleaned_deposit.json',
    'Data_Categorization/Cleaned_Data/cleaned_incoming_money.json',
    'Data_Categorization/Cleaned_Data/cleaned_payments.json',
    'Data_Categorization/Cleaned_Data/cleaned_Failed.json',
    'Data_Categorization/Cleaned_Data/cleaned_reversed.json',
    'Data_Categorization/Cleaned_Data/cleaned_third_party.json',
    'Data_Categorization/Cleaned_Data/cleaned_transfer.json',
    'Data_Categorization/Cleaned_Data/cleaned_withdraw.json',
    'Data_Categorization/Cleaned_Data/cleaned_Non_transaction.json',
    'Data_Categorization/Cleaned_Data/cleaned_payment_code_holders.json'
]

column_mappings = {
    "airtime": {
        "TransactionId": "TxId",
        "amount": "Amount",
        "currency": "CURRENCY",
        "Date": "Date",
        "Time": "TIME",
        "transaction_type": "Type",
        "current_balance": "Balance",
        "fee": "Fee"
    },
    "bundles": {
        "TransactionId": "TxId",
        "amount": "Amount",
        "currency": "CURRENCY",
        "Date": "Date",
        "Time": "TIME",
        "transaction_type": "Type",
        "current_balance": "Balance",
        "fee": "Fee"
    },
    "cashpower": {
        "TransactionId": "TxId",
        "token": "TOKEN",
        "amount": "Amount",
        "currency": "CURRENCY",
        "Date": "Date",
        "Time": "TIME",
        "transaction_type": "Type",
        "current_balance": "Balance",
        "fee": "Fee"
    },
    "payments": {
        "receiver": "RECEIVER",
        "TransactionId": "TxId",
        "amount": "AMOUNT",
        "currency": "CURRENCY",
        "Date": "Date",
        "Time": "TIME",
        "transaction_type": "Type",
        "current_balance": "Balance",
        "fee": "Fee"
    },
    "failedtransactions": {
        "receiver": "RECEIVER",
        "amount": "AMOUNT",
        "currency": "CURRENCY",
        "Date": "Date",
        "Time": "TIME",
        "transaction_type": "Type",
        "fee": "Fee"
    },
    "reversedtransactions": {
        "receiver": "RECEIVER",
        "amount": "AMOUNT",
        "currency": "CURRENCY",
        "Date": "Date",
        "Time": "TIME",
        "transaction_type": "Type",
        "current_balance": "BALANCE",
        "fee": "Fee",
        "phone_number": "PHONE_NUMBER"
    },
    "thirdparty": {
        "third_party_sender": "SENDER",
        "amount": "AMOUNT",
        "currency": "CURRENCY",
        "Date": "Date",
        "Time": "TIME",
        "transaction_type": "Type",
        "current_balance": "Balance",
        "fee": "Fee"
    },
    "withdraw": {
        "agent": "AGENT",
        "amount": "AMOUNT",
        "currency": "CURRENCY",
        "Date": "Date",
        "Time": "TIME",
        "transaction_type": "Type",
        "current_balance": "Balance",
        "fee": "Fee"
    },
    "nontransaction": {
        "number": "NUMBER"
    },
    "incomingmoney": {
        "sender": "SENDER",
        "amount": "AMOUNT",
        "currency": "CURRENCY",
        "Date": "Date",
        "Time": "TIME",
        "transaction_type": "Type",
        "current_balance": "Balance",
        "fee": "Fee"
    },
    "transfer": {
        "receiver": "RECEIVER",
        "phone_number": "PHONE_NUMBER",
        "amount": "AMOUNT",
        "currency": "CURRENCY",
        "Date": "Date",
        "Time": "TIME",
        "transaction_type": "Type",
        "current_balance": "Balance",
        "fee": "Fee"
    },
    "deposit": {
        "amount": "AMOUNT",
        "currency": "CURRENCY",
        "Date": "Date",
        "Time": "TIME",
        "transaction_type": "Type",
        "current_balance": "Balance",
        "fee": "Fee"
    },
    "codeholders": {
        "receiver": "RECEIVER",
        "code": "CODE",
        "TransactionId": "TxId",
        "amount": "AMOUNT",
        "currency": "CURRENCY",
        "Date": "Date",
        "Time": "TIME",
        "transaction_type": "Type",
        "current_balance": "Balance",
        "fee": "Fee"
    }
}

file_to_table_mapping = {
    'cleaned_Airtime.json': 'airtime',
    'cleaned_Bundles.json': 'bundles',
    'cleaned_cash_power.json': 'cashpower',
    'cleaned_deposit.json': 'deposit',
    'cleaned_incoming_money.json': 'incomingmoney',
    'cleaned_payments.json': 'payments',
    'cleaned_Failed.json': 'failedtransactions',
    'cleaned_reversed.json': 'reversedtransactions',
    'cleaned_third_party.json': 'thirdparty',
    'cleaned_transfer.json': 'transfer',
    'cleaned_withdraw.json': 'withdraw',
    'cleaned_Non_transaction.json': 'nontransaction',
    'cleaned_payment_code_holders.json': 'codeholders'
}



for file in json_files:
    try:
        file_name = file.split('/')[-1]
        table_name = file_to_table_mapping.get(file_name)

        if not table_name:
            print(f"Table name not found for file: {file_name}")
            continue

        if file == 'Data_Categorization/Cleaned_Data/cleaned_Non_transaction.json':
            print("====================================" + table_name + "====================================")
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                number_of_objects = len(data)
            print(number_of_objects, end="\n\n")
            cursor.execute("INSERT INTO nontransaction (NUMBER) VALUES (%s)", (number_of_objects,))
        else:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print("====================================" + table_name + "====================================")
                print(data, end="\n\n")
                if table_name in column_mappings:
                    data = [i for i in data if i.get('Date') != 'Unknown']
                    data.sort(key=lambda x: datetime.datetime.strptime(x['Date'], '%Y-%m-%d'), reverse=True)
                    for i in data:
                        if 'Unknown' in i.values():
                            continue
                        
                        if i.get('Date'):
                            i['Date'] = datetime.datetime.strptime(i['Date'].replace('/', '-'), '%Y-%m-%d').date()
                        if i.get('Time'):
                            i['Time'] = datetime.datetime.strptime(i['Time'], '%H:%M:%S').time()

                        mapped_data = {column_mappings[table_name][key]: value for key, value in i.items() if key in column_mappings[table_name]}

                        columns = ', '.join(mapped_data.keys())
                        placeholders = ', '.join(['%s'] * len(mapped_data))
                        print("====================================" + table_name + "====================================")
                        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

                        cursor.execute(sql, list(mapped_data.values()))
    except Exception as e:
        print(f"Error occured: {e}")
        continue

conn.commit()
cursor.close()
conn.close()