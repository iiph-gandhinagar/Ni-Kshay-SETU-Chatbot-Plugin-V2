import pandas as pd
import os

from app.slack_alerts.error_via_slack_alerts import send_slack_alert


from dotenv import load_dotenv
load_dotenv()



def second_ordering(first_ordering_node_ids, cadre, df):
    try:
        environment = os.getenv('APP_ENV') 
        cadre_df = df[df['cadre_id'].apply(lambda x: str(cadre) in x.split(',') if pd.notna(x) and x.strip() != '' else False)]

        # Create a set of node IDs associated with the cadre for quick lookup
        cadre_node_ids = set(cadre_df['node_id'])

        # Prioritize node IDs that are associated with the cadre
        cadre_first = [node_id for node_id in first_ordering_node_ids if node_id in cadre_node_ids]
        others = [node_id for node_id in first_ordering_node_ids if node_id not in cadre_node_ids]
        
        # Combine the lists, with cadre-associated IDs first
        ordered_node_ids = cadre_first + others
        return ordered_node_ids
    except Exception as e:
        print(f"Error in second_ordering: {e}")
        error_message = (
            f"Application: Ni-kshay SETU v3-Chatbot\n"
            f"ENV: {environment}\n"
            f"file: second_ordering.py\n"
            f"Error: {e}\n"

        )
        send_slack_alert(error_message)
