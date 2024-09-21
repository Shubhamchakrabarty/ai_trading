# access_token.py

import os
import sys
from fyers_apiv3 import fyersModel

# Get CLIENT ID and SECRET KEY

with open('client_id.txt', 'r') as file:
    # Read the content of the file
    got_client_id = file.read()

with open('secret_key.txt', 'r') as file:
    # Read the content of the file
    got_secret_key = file.read()

def generate_access_token(auth_code):
    # Use the auth_code variable as needed
    print(f"Received auth_code in access_token.py: {auth_code}")

    # Import the required module from the fyers_apiv3 package
    
    # from fyers_apiv3 import fyersModel

    # Define your Fyers API credentials
    client_id = got_client_id  # Replace with your client ID
    secret_key = got_secret_key  # Replace with your secret key
    redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"  # Replace with your redirect URI
    response_type = "code" 
    grant_type = "authorization_code" 

    # Create a session object to handle the Fyers API authentication and token generation
    session = fyersModel.SessionModel(
        client_id=client_id,
        secret_key=secret_key, 
        redirect_uri=redirect_uri, 
        response_type=response_type, 
        grant_type=grant_type
    )

    # Set the authorization code in the session object
    session.set_token(auth_code)

    # Generate the access token using the authorization code
    response = session.generate_token()

    access_token = response['access_token']

    print('Access Token is: ')
    print(access_token)

    a = open("access.txt", 'w')
    a.write(access_token)
    a.close()

if __name__ == '__main__':
    # Check if the script is run directly
    if len(sys.argv) > 1:
        # If command line arguments are provided, assume the first argument is the auth_code
        auth_code = sys.argv[1]
        generate_access_token(auth_code)
