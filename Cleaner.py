import re
import os
import xml.etree.ElementTree as ET
import json
import datetime

os.makedirs('Data_Categorization/Cleaned_Data', exist_ok=True)

def extract_data(body_text, filename):
    data = {}
    amount_pattern = re.compile(r'\b(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(RWF)\b')
    date_pattern = re.compile(r'(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})')
    transaction_type_pattern = re.compile(r'\b(received|payment|withdraw|deposit|transfer|purchase|bundle|cash power)\b', re.IGNORECASE)
    transaction_Id = re.compile(r'(TxId|Transaction ID|Financial Transaction Id|Transaction Id)[:\s]+(\w+)', re.IGNORECASE)
    receiver_pattern = re.compile(r'transferred to\s+([\w\s]+?)\s+\((\d+)\)|to\s+([\w\s]+?)\s+with token', re.IGNORECASE)
    current_balance_pattern = re.compile(r'New\s+balance\s*:\s*([\d,]+)\s*RWF|Your\s+new\s+balance\s*:\s*([\d,]+)\s*RWF', re.IGNORECASE)
    sender_pattern = re.compile(r'received\s+\d+\s+RWF\s+from\s+([\w\s]+?)\s+\(\*+\d+\)', re.IGNORECASE)
    third_party_sender_pattern = re.compile(r'by\s+([\w\s]+?)\s+on your MOMO account', re.IGNORECASE)
    cash_power_token = re.compile(r'with token\s+([\d-]+)', re.IGNORECASE)
    fee_pattern = re.compile(r'\bfee\b.*?(\d+(?:,\d{3})*(?:\.\d{2})?)', re.IGNORECASE)
    agent = re.compile(r'Agent:\s+([\w\s]+)', re.IGNORECASE)
    # reversed data
    reversed_names = re.compile(r'to\s+([\w\s]+?)\s+\((\d+)\)|to\s+([\w\s]+?)\s+with token', re.IGNORECASE)
    balance_reversed = re.compile(r'Your\s+new\s+balance\s+is\s*([\d,]+)\s*RWF', re.IGNORECASE)
    failed_transaction_pattern = re.compile(
        r'amount\s+(\d+)\s+RWF\s+for\s+([\w\s]+)\s+with\s+message:\s+([\d\w\s]+)\s+failed\s+at\s+(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})',
        re.IGNORECASE
    )
    code_holders_names_codes = re.compile(r'to\s+([\w\s\w\s]+?)\s+(\d+)')
    receiver_payment = re.compile(r'to\s+([\w\s\w\s]+?)\s+(with token)')

    if filename == 'transfer.xml':
        receiver_match = receiver_pattern.search(body_text)
        if receiver_match:
            data['receiver'] = receiver_match.group(1) or receiver_match.group(3)
            data['phone_number'] = ('+' + receiver_match.group(2)) if receiver_match.group(2) else 'Unknown'
        else:
            data['receiver'] = 'Unknown'
            data['phone_number'] = 'Unknown'
    

    if filename == "payment_code_holders.xml":
        receiver_match = code_holders_names_codes.search(body_text)
        if receiver_match:
            data['receiver'] = receiver_match.group(1)
            data['code'] = int(receiver_match.group(2))
        else:
            data['receiver'] = 'Unknown'
            data['code'] = 0
    
    if filename == "payments.xml":
        receiver_match = receiver_payment.search(body_text)
        if receiver_match:
            data['receiver'] = receiver_match.group(1)
        else:
            data['receiver'] = 'Unknown'

    if filename == 'incoming_money.xml':
        sender_match = sender_pattern.search(body_text)
        data['sender'] = sender_match.group(1) if sender_match else 'Unknown'
    
    if filename == 'cash_power.xml':
        token_match = cash_power_token.search(body_text)
        data['token'] = token_match.group(1) if token_match else 'Unknown'
    
    if filename == 'third_party.xml':
        third_party_sender_match = third_party_sender_pattern.search(body_text)
        data['third_party_sender'] = third_party_sender_match.group(1) if third_party_sender_match else 'Unknown'
    
    if filename == 'withdraw.xml':
        agent_match = agent.search(body_text)
        data['agent'] = agent_match.group(1) if agent_match else 'Unknown'
    
    if filename == 'Failed.xml':
        failed_match = failed_transaction_pattern.search(body_text)
        if failed_match:
            data['receiver'] = failed_match.group(2)
            data['amount'] = int(failed_match.group(1))
            if "Data Bundle" in data['receiver'] or "Bundles and Packs" in data['receiver']:
                data['type'] = "data_purchase"
            else:
                data['type'] = "normal_transaction"
        else:
            data['receiver'] = 'MTN'
            data['amount'] = 0
            data['type'] = 'Mtn_Bundles'
    
    if filename in ["Airtime.xml", "Bundles.xml", "cash_power.xml", "payment_code_holders.xml", "payments.xml", "payments.xml"]:
        TransactionId_match = transaction_Id.search(body_text)
        data['TransactionId'] = TransactionId_match.group(2) if TransactionId_match else 'Unknown'
    
    amount_match = amount_pattern.search(body_text)
    if amount_match:
        amount = amount_match.group(1).replace(',', '')
        currency = amount_match.group(2)
        data['amount'] = int(amount)
        data['currency'] = currency
    else:
        data['amount'] = 0
        data['currency'] = 'Unknown'

    date_match = date_pattern.search(body_text)
    if date_match:
        date_string = date_match.group(1)
        data['Date'] = date_string
        time_string = date_match.group(2)
        data['Time'] = time_string
    else:
        data['Date'] = 'Unknown'
        data['Time'] = 'Unknown'

    transaction_type_match = transaction_type_pattern.search(body_text)
    if transaction_type_match:
        data['transaction_type'] = transaction_type_match.group().lower()
    else:
        if 'received' in body_text.lower() or ('a transaction of' in body_text.lower() and 'on your momo account' in body_text.lower()):
            data['transaction_type'] = 'received'
        elif 'payment' in body_text.lower():
            data['transaction_type'] = 'payment'
        elif 'withdraw' in body_text.lower():
            data['transaction_type'] = 'withdraw'
        elif 'deposit' in body_text.lower():
            data['transaction_type'] = 'deposit'
        elif 'transfer' in body_text.lower():
            data['transaction_type'] = 'transfer'
        elif 'purchase' in body_text.lower():
            data['transaction_type'] = 'purchase'
        elif 'bundle' in body_text.lower():
            data['transaction_type'] = 'purchase'
        elif 'cash power' in body_text.lower():
            data['transaction_type'] = 'purchase'
        elif 'failed' in body_text.lower() or filename == 'rest.xml':
            data['transaction_type'] = 'failed'
        else:
            data['transaction_type'] = 'unknown'
    
    if filename != "Failed.xml":

        current_balance_match = current_balance_pattern.search(body_text)
        if current_balance_match:
            current_balance = current_balance_match.group(1) or current_balance_match.group(2)
            current_balance = current_balance.replace(',', '')
            new_balance = int(current_balance.replace('RWF', ''))
            data['current_balance'] = new_balance
        else:
            data['current_balance'] = 0
    
    if filename == "reversed.xml":
        balance_reversed_match = balance_reversed.search(body_text)
        if balance_reversed_match:
            current_balance = balance_reversed_match.group(1)
            current_balance = current_balance.replace(',', '')
            data['current_balance'] = int(current_balance)
        else:
            data['current_balance'] = 0

        reversed_name_match = reversed_names.search(body_text)
        if reversed_name_match:
            data['receiver'] = reversed_name_match.group(1) or reversed_name_match.group(3)
            data['phone_number'] = ('+' + reversed_name_match.group(2)) if reversed_name_match.group(2) else 'Unknown'
            data['transaction_type'] = 'reversed'
        else:
            data['receiver'] = 'Unknown'
            data['phone_number'] = 'Unknown'

    fee_match = fee_pattern.search(body_text)
    data['fee'] = int(fee_match.group(1).replace(',', '')) if fee_match else 0

    return data

def process_file(input_filename, output_filename):
    with open(input_filename, 'r', encoding='utf-8') as file:
        content = file.read()

    wrapped_content = f"<root>{content}</root>"

    tree = ET.ElementTree(ET.fromstring(wrapped_content))
    root = tree.getroot()

    cleaned_data = []

    for element in root:
        if 'body' in element.attrib:
            body_text = element.attrib['body']
            extracted_data = extract_data(body_text, os.path.basename(input_filename))
            if extracted_data:
                cleaned_data.append(extracted_data)

    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=4)

# List of categorized files to process
categorized_files = [
    'Airtime.xml',
    'Bundles.xml',
    'cash_power.xml',
    'deposit.xml',
    'Failed.xml',
    'incoming_money.xml',
    'Non_transaction.xml',
    'payment_code_holders.xml',
    'payments.xml',
    'reversed.xml',
    'third_party.xml',
    'transfer.xml',
    'withdraw.xml',
]

for filename in categorized_files:
    input_path = os.path.join('Data_Categorization', filename)
    output_path = os.path.join('Data_Categorization', 'Cleaned_Data', f'cleaned_{filename.replace(".xml", ".json")}')
    process_file(input_path, output_path)

print("Data is Cleaned")