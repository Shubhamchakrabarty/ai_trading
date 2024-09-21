from flask import Flask, render_template, jsonify, request
from scripts.auth_code import generate_auth_code
import subprocess
from fyers_apiv3 import fyersModel
import json
import os
from flask import send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_auth_code')
def run_auth_code():
    try:
        generated_link = generate_auth_code()
        return jsonify({'link': generated_link})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/run_access_token', methods=['GET'])
def run_access_token():
    try:
        auth_code = request.args.get('auth_code')
        print(f"Received auth_code: {auth_code}")

        # Run the access_token.py script with auth_code as an argument
        result = subprocess.run(['python', 'scripts/access_token.py', auth_code], capture_output=True, text=True)

        print("Script Output:", result.stdout)
        print("Script Error:", result.stderr)

        # Return the result from the script
        return jsonify({'message': result.stdout})
    except Exception as e:
        return jsonify({'error': str(e)})
    



@app.route('/run_test')
def run_test():
    try:
        result = subprocess.run(['python', 'scripts/test.py'], capture_output=True, text=True)

        print("Script Output:", result.stdout)
        print("Script Error:", result.stderr)

        # Convert the string output to a dictionary
        response_data = json.loads(result.stdout)

        # Check if the response is successful
        if 's' in response_data and response_data['s'] == 'ok':
            name = response_data['data']['name']
            return jsonify({'status': 'success', 'name': name})
        else:
            return jsonify({'status': 'failure'})
    except Exception as e:
        return jsonify({'status': 'failure', 'error': str(e)})



@app.route('/test')
def test():
    try:
        with open('access.txt', 'r') as file:
            access_token = file.read()

        fyers = fyersModel.FyersModel(client_id='DO6J3QY4K2-100', is_async=False, token=access_token, log_path="")
        response = fyers.get_profile()

        if 's' in response and response['s'] == 'ok':
            return render_template('test/test.html', data=response['data'])
        else:
            return render_template('test/test.html', error=response['message'])
    except Exception as e:
        return render_template('test/test.html', error=str(e))
    
    #==========================================================================

    

    # Define the path to the JSON configuration file
target_stoploss_config_file_path = os.path.join(os.path.dirname(__file__), 'target_stoploss_config.json')


def load_config():
    # Load configuration from the JSON file
    try:
        with open(target_stoploss_config_file_path, 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        return {'target': None, 'stoploss': None}

def save_config(target, stoploss):
    # Save configuration to the JSON file
    config = {'target': target, 'stoploss': stoploss}
    with open(target_stoploss_config_file_path, 'w') as config_file:
        json.dump(config, config_file)

@app.route('/submit_target_stoploss_values', methods=['POST'])
def submit_target_stoploss_values():
    try:
        # Get the target and stoploss values from the form submission
        target = float(request.form['target'])
        stoploss = float(request.form['stoploss'])

        # Save the values to the JSON configuration file
        save_config(target, stoploss)

        # Reload the page to display the updated values
        return render_template('operations/set_target_stoploss_values.html', current_target=target, current_stoploss=stoploss)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/operations/set_target_stoploss_values')
def target_stoploss_values():
    # Load the current configuration
    config = load_config()

    print(config)

    # Render the template with the current values
    return render_template('operations/set_target_stoploss_values.html', current_target=config['target'], current_stoploss=config['stoploss'])


#=============================================================================================

@app.route('/operations/target_stoploss')
def semd_target_stoploss_values():
    # Load the current configuration
    config = load_config()

    print(config)

    # Render the template with the current values
    return render_template('operations/target_stoploss.html', current_target=config['target'], current_stoploss=config['stoploss'])

#=============================================================================================

#  Target Stoploss FIRE!

@app.route('/run_fire_target_stoploss', methods=['GET'])
def run_fire_target_stoploss():
    try:
        # Assuming fire_target_stoploss.py is in the fyers/scripts directory
        # script_path = os.path.join(os.path.dirname(__file__), 'fyers/scripts/fire_target_stoploss.py')
        script_path = "scripts/fire_target_stoploss.py"

        # Run the fire_target_stoploss.py script
        result = subprocess.run(['python', script_path], capture_output=True, text=True)

        print("Script Output:", result.stdout)
        print("Script Error:", result.stderr)

        # You can customize the response based on the success or failure of the script
        if result.returncode == 0:
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'failure', 'error': result.stderr})

    except Exception as e:
        return jsonify({'status': 'failure', 'error': str(e)})

#=========================================================================================================        

# EXIT ALL POSITIONS

@app.route('/run_exit_all_positions', methods=['GET'])
def exit_all_positiions():
    script_path = "scripts/exit_all_positions.py"
    result = subprocess.run(['python', script_path], capture_output=True, text=True)
    print(result)
    return render_template('operations/ops.html')

#=======================================================================================================================
@app.route('/<section>/<page>')
def dynamic_route(section, page):
    template_name = f"{section}/{page}.html"
    return render_template(template_name)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')



