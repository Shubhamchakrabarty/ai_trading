# scripts/auth_code.py

from fyers_apiv3 import fyersModel

# Get CLIENT ID and SECRET KEY

with open('client_id.txt', 'r') as file:
    # Read the content of the file
    got_client_id = file.read()

with open('secret_key.txt', 'r') as file:
    # Read the content of the file
    got_secret_key = file.read()

# DEFINE THE FUNCTION

def generate_auth_code():
    client_id = got_client_id
    secret_key = got_secret_key
    redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"
    response_type = "code"  
    state = "sample_state"

    # Create a session model with the provided credentials
    session = fyersModel.SessionModel(
        client_id=client_id,
        secret_key=secret_key,
        redirect_uri=redirect_uri,
        response_type=response_type
    )

    # Generate the auth code using the session model
    response = session.generate_authcode()

    # Print the auth code received in the response
    print(secret_key)
    print(response)

    # Return the auth code as a string
    return response

# CALL THE generate_auth_code() FUNCTION

generate_auth_code()