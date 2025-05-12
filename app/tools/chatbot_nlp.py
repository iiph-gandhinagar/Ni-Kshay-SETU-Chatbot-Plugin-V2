import os
import re
import random
from nltk.chat.util import Chat


from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import Pinecone as LangChainPinecone

from pinecone import Pinecone

from sentence_transformers import SentenceTransformer, util

from app.slack_alerts.error_via_slack_alerts import send_slack_alert

from dotenv import load_dotenv
load_dotenv()


environment = os.getenv("APP_ENV")

# Initialize Pinecone



class CustomChat(Chat):
    def __init__(self, pairs):
        # Initialize with pairs
        print(type(pairs))
        self._pairs = pairs  # Ensure this matches with how you store and reference pairs

    def respond(self, user_input):

        user_input = user_input.strip()
        
        for pattern, responses in self._pairs:  # Corrected from _singles to _pairs
            pattern = pattern.strip()
            match = re.search(pattern, user_input, re.IGNORECASE)
            

            if match:
                response = random.choice(responses)  # Choose a random response
                if match.groups():
                    response = response.format(*match.groups())
                return response
        return "I'm not sure I understand you fully."


pairs_static_list = [

    [r"^(okay|ok|alright|ok alright|okay alright)$",
     ["Got it! If you need anything else, just let me know.",
      "Alright! I'm here if you have more questions.",
      "Okay! Is there anything else I can assist you with today?",
      "Great! Let me know if there’s more I can help you with.",
      ]],
]
def chatbot_response_static(user_input):

        chat_static = CustomChat(pairs_static_list)
        return chat_static.respond(user_input)


def is_fallback_query(user_question, user_fallback_phrases):
    # Encode user input and fallback phrases
    model = SentenceTransformer(os.getenv('SENTENCE_TRANSFORMER_MODEL'))

    user_embedding = model.encode(user_question, convert_to_tensor=True)
    phrase_embeddings = model.encode(user_fallback_phrases, convert_to_tensor=True)

    # Compute cosine similarity
    similarities = util.pytorch_cos_sim(user_embedding, phrase_embeddings)
    
    # If similarity is high for any phrase, consider it a fallback
    return similarities.max().item() > 0.75  # Adjust threshold as needed

# Function to handle user input and generate response
def chatbot_response(user_question):
    try:
    # if 
        pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

        # Connect to Pinecone index
        index_name = os.getenv("SYSTEM_QA_INDEX_NAME")

        # Initialize embedding model and LLM
        embeddings = HuggingFaceEmbeddings(model_name=os.getenv('VECTOR_MODEL'))
        llm = ChatOpenAI(model="gpt-4o-mini")

        # Create vector store once
        vectorstore = LangChainPinecone.from_existing_index(index_name=index_name, embedding=embeddings, text_key="text")

        # Create retrieval chain once
        retrieval_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 6})
        )
        result_static=chatbot_response_static(user_question)
        if result_static == "I'm not sure I understand you fully.":
            

    
            # List of fallback phrases to check for
            user_fallback_phrases = [
                'tell me more', 'tell me about', 'elaborate further','please elaborate' ,
                'can you elaborate', 'give me more information', 
                'what else', 'expand on that', 'can you explain more',
                'i want to read about', 'i want to know about', 'i want to learn about',
                'can you tell me about', 'show me more about', 'i would like to read about',
                'i want to take a test', 'i want to take quiz', 'want to test my knowledge', 'can you test my knowledge',
                'knowledge quiz', 'i want to raise a query','query response',
                'i want to see my queries', 'i have a patient with coughing symptoms','patient with symptoms',
                'i have a patient'
            ]
            if is_fallback_query(user_question, user_fallback_phrases):
            # Check if the user's question contains any of the fallback phrases
                return "I don't know"

            # Retrieve answer
            response = retrieval_chain.run(user_question)
            if "test my knowledge on tb" in user_question or "manage tb" in user_question:
                return"I don't know"
            
            response_fallback_phrases = ['i don\'t know.', 'sorry', 'i could not find','I\'m sorry','I\'m sorry,','could you please', 'could']
            # If the response is empty or irrelevant, return a fallback message
            if is_fallback_query(response,response_fallback_phrases) :
                return "I don't know"
            if "i dont know" in response or "sorry" in response:
                return "I don't know"
            # print('response',response)
            return response
        else:
            return result_static
    except Exception as e:
        print(f"Error occurred while handling user input: {str(e)}")
        error_message = (
            f"Application: Ni-kshay SETU v3-Chatbot-system tool\n"
            f"ENV: {environment}\n"
            f"file: chatbot_nlp.py\n"
            f"Error: {e}\n"
        )
        send_slack_alert(error_message)
  



