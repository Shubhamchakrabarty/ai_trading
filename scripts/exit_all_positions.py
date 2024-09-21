from fyers_apiv3 import fyersModel

# client_id = "XC4XXXXM-100"
# access_token = "eyJ0eXXXXXXXX2c5-Y3RgS8wR14g"

# CLIENT ID And ACCESS TOKEN

# client_id = "DO6J3QY4K2-100"

# Define the Exit all positions function 
def exit_all_positions():
    with open('client_id.txt', 'r') as file:
        # Read the content of the file
        client_id = file.read()
        print(client_id)

    # Get access token from access.txt the file
    with open('access.txt', 'r') as file:
        # Read the content of the file
        access_token = file.read()

    # Initialize the FyersModel instance with your client_id, access_token, and enable async mode
    fyers = fyersModel.FyersModel(client_id=client_id, token=access_token,is_async=False, log_path="")

    data = {}

    response = fyers.exit_positions(data=data)

    print(response)
    return response


# RUN the Exit All Positions Function\

exit_all_positions()
