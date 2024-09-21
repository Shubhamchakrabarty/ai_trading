import asyncio
from fyers_apiv3 import fyersModel
import json
import subprocess
import sys

#=== === === === === === === === === === === ===
#====== SET TARGET - STOPLOSS % HERE =============

# Read variables from the JSON file
with open('target_stoploss_config.json', 'r') as json_file:
    target_stoploss_data_received = json.load(json_file)

target_percentage = target_stoploss_data_received["target"]
stop_loss_percentage = target_stoploss_data_received["stoploss"]

# Or Hardcoded

# target_percentage = 1.5
# stop_loss_percentage = 1.5

#=============================================
#=============================================
#=============================================

# CLIENT ID And ACCESS TOKEN

# client_id = "DO6J3QY4K2-100"

with open('client_id.txt', 'r') as file:
    # Read the content of the file
    client_id = file.read()

# Get access token from access.txt the file
with open('access.txt', 'r') as file:
    # Read the content of the file
    access_token = file.read()

# Run xyz.py using subprocess
# subprocess.run(['python', 'scripts/modify.py'])
    
# access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE3MDE5MTAyMzUsImV4cCI6MTcwMTk5NTQzNSwibmJmIjoxNzAxOTEwMjM1LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCbGNSYmJzZHB5aVA4UkZlM0lDT0FoYnhzNTh5eGprLVptMWRNUU1wVmdPVnZwaXg3ZHlJckVxSkhzdDZ6MUl6RWJoSEVrUHlvR0NPMmllRDNMWjZzWnRXMkdwVjdTUmFLand3VUNKd3FsOHJHV2FPST0iLCJkaXNwbGF5X25hbWUiOiJTSFVCSEFNIENIQUtSQUJBUlRZIiwib21zIjoiSzEiLCJoc21fa2V5IjoiYjlkOGZmYmUzZmZhYjJmZjBmOTBjNWJhOTcxMDRhOTFmZWMzYzEzZjUxYzlkZDE3YjFmMjEwYzIiLCJmeV9pZCI6IllTMDA3NDMiLCJhcHBUeXBlIjoxMDAsInBvYV9mbGFnIjoiTiJ9.ulWcwuD1Z1aDhNR_T4Ve7HOIpy-vHKCtkhFhWp4wXMM"

# Initialize the FyersModel instance with your client_id, access_token, and enable async mode
fyers = fyersModel.FyersModel(client_id=client_id, token=access_token,is_async=False, log_path="")

response = fyers.orderbook()

# Extract the last 3 orders
last_3_orders = response['orderBook'][-3:]

# print(last_3_orders)
# sys.exit()

# Extract Buy, Stop Loss, and Target orders
buy_order = next(order for order in last_3_orders if order['id'].endswith("BO-1"))
stop_loss_order = next(order for order in last_3_orders if order['id'].endswith("BO-2"))
target_order = next(order for order in last_3_orders if order['id'].endswith("BO-3"))

# Extract relevant information
buy_price = buy_order['limitPrice']
quantity = buy_order['qty']
stop_loss_order_id = stop_loss_order['id']
target_order_id = target_order['id']


# Calculate target and stop-loss prices (rounded to nearest 0.05)
target_price = round(buy_price * (1 + target_percentage / 100), 2)
target_price = round(round(target_price / 0.05) * 0.05, 2)

# target_trigger_price = round(target_price + 0.05, 2)

stop_loss_price = round(buy_price * (1 - stop_loss_percentage / 100), 2)
stop_loss_price = round(round(stop_loss_price / 0.05) * 0.05, 2)

stop_loss_trigger_price = round(stop_loss_price + 0.05, 2)

# Print the results
print(f"Buy Price: {buy_price:}")
print(f"Target Price: {target_price:}")
print(f"Stop Loss Price: {stop_loss_price:}")
print(f"Stop Loss Trigger Price: {stop_loss_trigger_price:}")

#=====  MODIFY SECTION ==============

# Variables to pass to xyz.py
data_to_pass = {
    "target_order_id": target_order_id,
    "stop_loss_order_id": stop_loss_order_id,
    "target_price": target_price,
    "stop_loss_price": stop_loss_price,
    "stop_loss_trigger_price": stop_loss_trigger_price,
    "quantity": quantity
    # Add other variables as needed
}

# Write variables to a JSON file
with open('scripts/modification_details_config.json', 'w') as json_file:
    json.dump(data_to_pass, json_file)

# Run xyz.py using subprocess
subprocess.run(['python', 'scripts/modify.py'])