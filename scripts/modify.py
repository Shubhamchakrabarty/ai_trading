import asyncio
from fyers_apiv3 import fyersModel
import json

# Read variables from the JSON file
with open('scripts/modification_details_config.json', 'r') as json_file:
    data_received = json.load(json_file)

# CLIENT ID And ACCESS TOKEN

# client_id = "DO6J3QY4K2-100"

with open('client_id.txt', 'r') as file:
    # Read the content of the file
    client_id = file.read()

# Get access token from access.txt the file
with open('access.txt', 'r') as file:
    # Read the content of the file
    access_token = file.read()
# access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE3MDE5MTAyMzUsImV4cCI6MTcwMTk5NTQzNSwibmJmIjoxNzAxOTEwMjM1LCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCbGNSYmJzZHB5aVA4UkZlM0lDT0FoYnhzNTh5eGprLVptMWRNUU1wVmdPVnZwaXg3ZHlJckVxSkhzdDZ6MUl6RWJoSEVrUHlvR0NPMmllRDNMWjZzWnRXMkdwVjdTUmFLand3VUNKd3FsOHJHV2FPST0iLCJkaXNwbGF5X25hbWUiOiJTSFVCSEFNIENIQUtSQUJBUlRZIiwib21zIjoiSzEiLCJoc21fa2V5IjoiYjlkOGZmYmUzZmZhYjJmZjBmOTBjNWJhOTcxMDRhOTFmZWMzYzEzZjUxYzlkZDE3YjFmMjEwYzIiLCJmeV9pZCI6IllTMDA3NDMiLCJhcHBUeXBlIjoxMDAsInBvYV9mbGFnIjoiTiJ9.ulWcwuD1Z1aDhNR_T4Ve7HOIpy-vHKCtkhFhWp4wXMM"

# Access the variables
target_order_id = data_received["target_order_id"]
stop_loss_order_id = data_received["stop_loss_order_id"]
target_price = data_received["target_price"]
stop_loss_price = data_received["stop_loss_price"]
stop_loss_trigger_price = data_received["stop_loss_trigger_price"]
quantity = data_received["quantity"]
# Access other variables as needed

# Initialize the FyersModel instance with your client_id, access_token, and enable async mode
fyers = fyersModel.FyersModel(client_id=client_id, token=access_token, is_async=True, log_path="")

async def modify_order():
    orderId = stop_loss_order_id
    data = {
        "id": orderId, 
        "type": 4, 
        "limitPrice": stop_loss_price,
        "stopPrice": stop_loss_trigger_price,
        "qty": quantity
    }

    response = await fyers.modify_order(data=data)
    print(response)

asyncio.run(modify_order())

async def modify_order():
    orderId = target_order_id
    data = {
        "id": orderId, 
        "type": 1, 
        "limitPrice": target_price,
        "qty": quantity
    }

    response = await fyers.modify_order(data=data)
    print(response)

asyncio.run(modify_order())
