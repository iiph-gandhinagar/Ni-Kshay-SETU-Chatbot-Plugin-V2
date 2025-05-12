

import os

from transformers import AutoTokenizer, AutoModel
import torch

from pinecone import Pinecone

from app.slack_alerts.error_via_slack_alerts import send_slack_alert

from dotenv import load_dotenv
load_dotenv()

def vectors_search(query):
    try:
        environment = os.getenv('APP_ENV')
        api_key = os.getenv('PINECONE_API_KEY')  # Replace with your actual Pinecone API Key
        pinecone = Pinecone(api_key=api_key, environment = os.getenv('PINECONE_ENV'))

        index_name = os.getenv('CHATBOT_INDEX_NAME')

        index = pinecone.Index(index_name)

        tokenizer = AutoTokenizer.from_pretrained(os.getenv('VECTOR_MODEL'))
        model = AutoModel.from_pretrained(os.getenv('VECTOR_MODEL'))

        similarity_threshold = 0.4

        inputs = tokenizer(query, return_tensors="pt", truncation=True, padding=True)

        # Generate embeddings (without gradient computation)
        with torch.no_grad():
            outputs = model(**inputs)

        # Mean pooling to create a sentence embedding
        query_vector = outputs.last_hidden_state.mean(dim=1).squeeze().tolist()

        response = index.query(vector=[query_vector], top_k=1000, include_metadata=True)  # Large top_k
        node_scores = []

        # Iterate over the matches
        for match in response['matches']:
            if match['score'] >= similarity_threshold:  # Only consider matches above the threshold
                node_id = match['metadata']['node_id']  # Extract node_id

                # Collect the node_id and its score
                node_scores.append((node_id, match['score']))

        # Sort by score in descending order (highest score first)
        node_scores.sort(key=lambda x: x[1], reverse=True)

        # Initialize an empty list to store unique node_ids
        unique_node_ids = []

        # Add only unique node_ids to the list, sorted by score
        for node_id, score in node_scores:
            if node_id not in unique_node_ids:
                if isinstance(node_id, float):
                    node_id = int(node_id) 
                unique_node_ids.append(node_id)

   
        return unique_node_ids
    except Exception as e:
        error_message = (
            f"Application: Ni-kshay SETU v3-Chatbot\n"
            f"ENV: {environment}\n"
            f"file:vector_search.py\n"
            f"Error: {e}\n"

        )
        send_slack_alert(error_message)
        print(f"An error occurred in vectors_search: {e}")