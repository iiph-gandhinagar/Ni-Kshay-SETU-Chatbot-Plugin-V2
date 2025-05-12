import os

from app.tasks.full_form_api import full_forms

from app.slack_alerts.error_via_slack_alerts import send_slack_alert

from dotenv import load_dotenv
load_dotenv()




def get_short_forms(query):
    try:
        environment = os.getenv('APP_ENV')
        short_forms_df = full_forms()
        match = short_forms_df[short_forms_df['title'].str.lower() == query.lower()]
        if not match.empty:
            full_form = [match[col].iloc[0] for col in match.columns if 'pattern' in col]
            return full_form
        return []
    except Exception as e:
        print("Error in get_short_forms:", str(e))
        error_message = (
            f"Application: Ni-kshay SETU v3-Chatbot\n"
            f"ENV: {environment}\n"
            f"file: short_to_full_form.py\n"
            f"Error: {e}\n"
        )
        send_slack_alert(error_message)
  

def match_full_form_with_node_id(full_forms, df):
    try:
        environment = os.getenv('APP_ENV')
        node_ids = []
        for full_form_query in full_forms:
            matched_titles = df[df['node_title'].str.contains(full_form_query, case=False, na=False)]
            if not matched_titles.empty:
                node_ids.extend(matched_titles['node_id'].tolist())
        return node_ids
    except Exception as e:
        print("Error in match_full_form_with_node_id:", str(e))
        error_message = (
            f"Application: Ni-kshay SETU v3-Chatbot\n"
            f"ENV: {environment}\n"
            f"file:short_to_full_form.py\n"
            f"Error: {e}\n"

        )
        send_slack_alert(error_message)
   
  