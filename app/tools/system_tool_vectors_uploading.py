import os 
import uuid

import requests

from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings

from pinecone import Pinecone, ServerlessSpec

from app.slack_alerts.error_via_slack_alerts import send_slack_alert

# Load environment variables from the .env file
from dotenv import load_dotenv
load_dotenv()

environment = os.getenv('APP_ENV')
# Initialize Pinecone
pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))  # You can also pass the API key directly here

# Function to split the extracted text into chunks
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=600,
        chunk_overlap=50,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

# Function to create vector store from text chunks using HuggingFaceEmbeddings
def get_vectorstore(text_chunks):
    try:
        embeddings = HuggingFaceEmbeddings(model_name=os.getenv('VECTOR_MODEL'))  # specify model
        vectors = embeddings.embed_documents(text_chunks)

        index_name = os.getenv("SYSTEM_QA_INDEX_NAME")

        if index_name not in pc.list_indexes().names():
            pc.create_index(
                name=index_name, 
                dimension=384,  # Dimension for sentence-transformers/all-MiniLM-L6-v2
                metric='cosine',  # Use cosine similarity for sentence embeddings
                spec=ServerlessSpec(cloud='aws', region='us-east-1')  # Adjust to your preferred cloud region
            )
        # Connect to Pinecone
        index = pc.Index(index_name)
        index_stats = index.describe_index_stats()

        if index_stats['total_vector_count'] > 0:
            print("Index is not empty, clearing the index...")
            index.delete(deleteAll=True)
        else:
            print("Index is already empty or does not exist.")

        # Prepare data for upsert (add unique ID for each chunk)
        upsert_data = [(str(uuid.uuid4()), vector, {"text": chunk}) for chunk, vector in zip(text_chunks, vectors)]

        # Upsert the vectors into Pinecone
        index.upsert(vectors=upsert_data)

        print("Embeddings stored in Pinecone successfully!")
    except Exception as e:
        print(f"Error occurred while creating vector store: {str(e)}")
        error_message = (
            f"Application: Ni-kshay SETU v3-Chatbot-system tool\n"
            f"ENV: {environment}\n"
            f"file:system_tool_vectors_uploading.py\n"
            f"Error: {e}\n"

        )
        send_slack_alert(error_message)
   


def process_api_data():
    api_url = f'{os.getenv("BASE_URL")}/api/system-question/get-all-system-questions'  # Expecting URL as query parameter

    if not api_url:
        return {"error": "Missing 'url' parameter"}, 400

    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()

            output_lines = []
            for index, item in enumerate(data.get('data', []), start=1):
                for q_index, question in enumerate(item.get('questions', []), start=1):
                    output_lines.append(f"{index}.{q_index}. {question.get('en', '')}")
                for a_index, answer in enumerate(item.get('answers', []), start=1):
                    output_lines.append(f"    {a_index}. {answer.get('en', '')}")

            # Format the output into a single string with newlines
            formatted_output = "\n".join(output_lines)

            # Split text into chunks
            text_chunks = get_text_chunks(formatted_output)

            # Store embeddings in Pinecone
            get_vectorstore(text_chunks)

            return { "success": "Embeddings stored in Pinecone successfully!"}, 200

        else:
            error_msg = (
                f"Application: Ni-kshay SETU v3-Chatbot-system tool\n"
                f"ENV: {environment}\n"
                f"file: system_tool_vectors_uploading.py\n"
                f"Error: Failed to fetch data from API. Status code: {response.status_code}\n"
                f"URL: {api_url}\n"
            )
            send_slack_alert(error_msg)
            return {"error": f"Failed to fetch data from API. Status code: {response.status_code}"}, 500

    except requests.exceptions.RequestException as e:
        error_msg = (
            f"Application: Ni-kshay SETU v3-Chatbot-system tool\n"
            f"ENV: {environment}\n"
            f"file: system_tool_vectors_uploading.py\n"
            f"Error: {e}\n"
            f"URL: {api_url}\n"
        )
        send_slack_alert(error_msg)
        return {"error": f"An error occurred while fetching the API: {str(e)}"}, 500


