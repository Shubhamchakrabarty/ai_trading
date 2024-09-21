# scripts/test.py

from fyers_apiv3 import fyersModel
import json

client_id = "DO6J3QY4K2-100"


# Open the file
with open('./access.txt', 'r') as file:
    # Read the content of the file
    access_token = file.read()

# Initialize the FyersModel instance with your client_id, access_token, and enable async mode
fyers = fyersModel.FyersModel(client_id=client_id, is_async=False, token=access_token, log_path="")

# Make a request to get the user profile information
response = fyers.get_profile()
# response2 = fyers.orderbook()
# print(response2)


# Print the response received from the Fyers API
print(json.dumps(response))