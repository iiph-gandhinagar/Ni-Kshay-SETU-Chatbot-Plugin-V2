import requests
import os

import pandas as pd

from app.slack_alerts.error_via_slack_alerts import send_slack_alert

from dotenv import load_dotenv
load_dotenv()


def full_forms():
    try:
        environment = os.getenv('APP_ENV')
        base_url = os.getenv('BASE_URL')
        api = f"{base_url}/api/abbreviation/get-all-abbreviation"
        response = requests.get(api)

        if response.status_code != 200:
            print(f"API Request Failed: {response.status_code}")
            error_msg = f"API Request Failed: {response.status_code}"
           
            error_message = (
                f"Application: Ni-kshay SETU v3-Chatbot\n"
                f"ENV: {environment}\n"
                f"file:full_form_api.py\n"
                f"Error: {error_msg}\n"

            )
            send_slack_alert(error_message)

        data = response.json()
        if not data.get('data'):
            print("Error: 'data' key missing or empty in API response")
            error_msg = "Error: 'data' key missing or empty in API response"
            error_message = (
                f"Application: Ni-kshay SETU v3-Chatbot\n"
                f"ENV: {environment}\n"
                f"file:full_form_api.py\n"
                f"Error: {error_msg}\n"
            )
            send_slack_alert(error_message)
                
                
        df = pd.json_normalize(data['data'])

        if 'patterns' in df.columns:
            # Split 'patterns' into separate columns
            patterns_df = df['patterns'].apply(lambda x: pd.Series(x))

            # Rename the new pattern columns
            patterns_df.columns = [f'pattern{col+1}' for col in patterns_df.columns]

            # Concatenate the original DataFrame with the new pattern columns
            df = pd.concat([df.drop(columns=['patterns']), patterns_df], axis=1)


        df = df.drop(columns=['_id','createdAt','updatedAt','__v'])
        return df
    except Exception as e:
        error_msg = f"Error occurred while fetching full forms: {str(e)}"

        error_message = (
            f"Application: Ni-kshay SETU v3-Chatbot\n"
            f"ENV: {environment}\n"
            f"file:full_form_api.py\n"
            f"Error: {e}\n"

        )
        send_slack_alert(error_message)
