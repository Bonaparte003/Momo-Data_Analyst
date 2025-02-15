import xml.etree.ElementTree as ET
import os

# Ensure the directory exists
os.makedirs('Data_Categorization', exist_ok=True)

tree = ET.parse(r'/mnt/c/Users/LENOVO/.vscode/MoMo-Data-Analysis/modified_sms_v2.xml')
root = tree.getroot()

incoming_money = []
payments = []
deposit = []
with_draw = []
Non_transaction = []
transfer = []
third_party = []
purchase = []
payment_code_holders = []
bank_deposit = []
Airtime = []
Bundles = []
cash_power = []
reversed = []
Failed = []

for element in root:
    # Check if 'body' attribute exists
    if 'body' in element.attrib:
        body_text = element.attrib['body'].lower()
        # Check if 'received' is in the body attribute
        if 'received' in body_text:
            incoming_money.append(ET.tostring(element, encoding='unicode'))
        # Check if 'payment' is in the body attribute
        elif 'payment' in body_text and 'failed' not in body_text:
            if 'cash power' in body_text and 'fee was 0 rwf.' in body_text:
                cash_power.append(ET.tostring(element, encoding='unicode'))
            elif 'fee was 0 rwf.' in body_text and 'airtime' in body_text:
                Airtime.append(ET.tostring(element, encoding='unicode'))
            elif 'fee was 0 rwf.' in body_text and 'airtime' not in body_text and 'bundle' not in body_text:
                payment_code_holders.append(ET.tostring(element, encoding='unicode'))
            elif 'bundle' in body_text:
                Bundles.append(ET.tostring(element, encoding='unicode'))
                
            else:
                payments.append(ET.tostring(element, encoding='unicode'))

        elif 'bank deposit' in body_text:
            deposit.append(ET.tostring(element, encoding='unicode'))
        elif 'withdraw' in body_text:
            with_draw.append(ET.tostring(element, encoding='unicode'))
        elif 'transfer' in body_text:
            transfer.append(ET.tostring(element, encoding='unicode'))
        elif '*164*s*y\'ello,a transaction of' in body_text:
            if 'bundle' in body_text:
                Bundles.append(ET.tostring(element, encoding='unicode'))
            third_party.append(ET.tostring(element, encoding='unicode'))
        elif 'yello!umaze kugura' in body_text:
            purchase.append(ET.tostring(element, encoding='unicode'))
        elif 'reversed' in body_text:
            reversed.append(ET.tostring(element, encoding='unicode'))
        elif 'failed' in body_text:
            Failed.append(ET.tostring(element, encoding='unicode'))
        else:
            Non_transaction.append(ET.tostring(element, encoding='unicode'))

# Write categorized data to files
def write_to_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(item)

write_to_file('Data_Categorization/incoming_money.xml', incoming_money)
write_to_file('Data_Categorization/payments.xml', payments)
write_to_file('Data_Categorization/deposit.xml', deposit)
write_to_file('Data_Categorization/withdraw.xml', with_draw)
write_to_file('Data_Categorization/transfer.xml', transfer)
write_to_file('Data_Categorization/third_party.xml', third_party)
write_to_file('Data_Categorization/payment_code_holders.xml', payment_code_holders)
write_to_file('Data_Categorization/cash_power.xml', cash_power)

# Combine Airtime and purchase lists before writing
Airtime.extend(purchase)
write_to_file('Data_Categorization/Airtime.xml', Airtime)
write_to_file('Data_Categorization/Bundles.xml', Bundles)
write_to_file('Data_Categorization/reversed.xml', reversed)
write_to_file('Data_Categorization/Failed.xml', Failed)
write_to_file('Data_Categorization/Non_transaction.xml', Non_transaction)