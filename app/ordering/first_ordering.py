import pandas as pd
import os

from app.slack_alerts.error_via_slack_alerts import send_slack_alert


from dotenv import load_dotenv
load_dotenv()

 

def extract_intent_keywords(query):
    # This function should extract the key intent and keywords from the query
    # For simplicity, here we just return the query split into words
    return query.lower().split()

def score_relevance(node_title, keywords):
    # A simple relevance scoring by counting keyword matches in the node title
    return sum(keyword in node_title.lower() for keyword in keywords)

def first_ordering(unique_node_ids, query, df):
    try:
        environment = os.getenv('APP_ENV')
        # Extract keywords or intent from the query
        keywords = extract_intent_keywords(query)

        # Prepare a list to hold scores and node IDs
        scored_nodes = []

        for node_id in unique_node_ids:

            filtered_df = df[df['node_id'] == node_id]

            if not filtered_df.empty:
                node_title = filtered_df['node_title'].iloc[0]
                if pd.isna(node_title):
                    continue  # Skip this node_id
                relevance_score = score_relevance(node_title, keywords)
                scored_nodes.append((node_id, relevance_score))
            else:
                print(f"No matching node found for node_id: {node_id}")

        
        # Sort nodes based on the calculated relevance score, highest first
        scored_nodes.sort(key=lambda x: x[1], reverse=True)
        # Return the sorted node IDs
        return [node_id for node_id, _ in scored_nodes]
    except Exception as e:
        error_message = (
            f"Application: Ni-kshay SETU v3-Chatbot\n"
            f"ENV: {environment}\n"
            f"file:first_ordering.py\n"
            f"Error: {e}\n"

        )
        send_slack_alert(error_message)
