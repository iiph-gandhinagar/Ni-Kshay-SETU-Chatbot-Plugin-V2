from app.tools.pinecone_testing import find_node_ids_ntep
from app.tools.no_response import no_response
from app.tools.no_response import agent_response
from app.tools.no_response import clarification_message
from app.tools.system_tool_vectors_uploading import process_api_data

from app.tools.tool_functions import greetings_tool
from app.tasks.gibberish_check_gateway import gateway_function

from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient
from app.slack_alerts.error_via_slack_alerts import send_slack_alert
import google.generativeai as genai

import os
import re

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
environment = os.getenv('APP_ENV')


class Query(BaseModel):
    text: str
    userid: str
    sessionid: str
    langcode: str
    selected_mode: str
    selected_option: int


client = MongoClient(os.getenv('MONGO_CLIENT'))
db = client[os.getenv("MONGO_DB")]
collection = db[os.getenv("MONGO_COLLECTION")]
session_context = {}

def main(query, sessionid):
    
    history = []
    document = collection.find_one({"sessionId": sessionid})

    if document is None:
        print(f"No document found for sessionId: {sessionid}")
        llm_history = []
    else:
        llm_history = document.get('llm_history', [])
        for questions in llm_history:
            history_data = [{
                "role": "user",
                "parts": [
                    questions.get('question')
                ],
            }, {
                "role": "model",
                "parts": [
                    questions.get('answer')
                ],


            }]

            history.extend(history_data)
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    generation_config = {
        "temperature": int(os.getenv('MODEL_CONFIG_temp')),
        "top_p": float(os.getenv('MODEL_CONFIG_TOP_P')),
        "top_k": int(os.getenv('MODEL_CONFIG_TOP_K')),
        "max_output_tokens": int(os.getenv('MAX_OUTPUT_TOKENS')),
        "response_mime_type": os.getenv('RESPONSE_MIME_TYPE'),
    }
    
    instructions = f"""
        Classify the intent of the following query and select the most appropriate module:

        Modules available:
        1. Prescription Generator: Only for queries explicitly related to generating medical prescriptions. Keywords include ['patient', 'prescription', 'medication', 'dosage', 'treatment', 'regimen', 'managetb','manage tb india'] if the query include any of these keywords always return this module name .
        2. Assessment: Its a quiz module for testing user's knowledge. Keywords include ['test knowledge about TB','quiz', 'test', 'evaluate', 'exam', 'questions', 'trivia', 'knowledge quiz'] if the query include any of these keywords always return this module name .
        3. Query Response: For queries about raising tickets, getting support, or help related to tuberculosis information and patient cases only. Keywords inclue ['query','review','support','opinion','assistance','consult','consultation,'resolution','care','adjustments', 'help','discussion','query2coe','query 2coe'] if the query include any of these keywords always return this module name.
        4. NTEP: Strictly Tailored for inquiries specifically related to tuberculosis(tb) or NTEP functions,any kind of short forms or abbreviations and other health-related terms only. This module is essential for addressing detailed questions about tuberculosis treatments and diagnostics or NTEP functions, offering direct response from the function for further information where applicable.Dont anwers questions which are not related to ntep or tuberculosis , and other health-related terms always return the response from the module
        5. Tech Support: Strictly for mobile application related queries.
        6. Greetings: Striclty For casual greetings and acknowledgments like 'hello', 'hi', 'thank you'. Also if someone types just their names handle it not for tb related question at all.
        7. NoResponse: For any questions outside tuberculosis or health i.e. maths, weather, calendar, news, abusive, informal language etc. Provide a polite response random not same all the time letting them know  that it is outside of your context.

        Query: "{query}"

        Reasoning steps:
        1. Analyze the query for explicit keywords or phrases matching the module descriptions as each module has there keywords mentioned in their descriptions please keep that in mind if you find a query with matching keyowrds pass that modules name.
        2. Select the most relevant single module based on the query content.Always select the module and pass it as response do not answer yourself or improvise yourself choose not to respond and politely tell the user you dont know.
        3. Output the selected single module telling the user that they mean this module or something like that and passing the as the module name in your response dont expand the response by adding unnecessary long sentences keep it very short adn simple and as you have access of the chat history you will know what the user means when they ask more about the asked query so you would know thw context through the chat history that yes the user is talking about this .keep it very short and simple  as it may happen that you might feel that some user queries can be answered from multiple modules at that time you can ask the user letting them know in good language that more than 1 module can answer their question which do they prefer you are a language model you know how to handle that right but always keep it short once the user confirms they want that module just give them that dont ask unnecessary questions .
        4. If the selected module is Greetings or NoResponse you already know how to have a converstion with the user giving them reponse as a polite chatbot by understanding the query you are smart enough. and only reutrn the response for these 2 modules in str dont return there names.
        5. Whenever asked about yourself as who you are or who made you then frame a nice answer as you are a Niksay Setu chatbot designed by that team and developed the smart engineers improvise your response every time dont give same sentence in response but always keep in mind you are a Nikshay Setu chatbot designed for answering tb related questions and nikshay setu app related questions only if it seems that user query is out of this context please tell them politely and as you are smart enough you know how to improvise each response you give so the user doesnt feel that the response is machine generated.
        6. Lastly you should know that NTEP is your fallback module so if it seems that the user query cant be answered from any of the module specified you can repond with ntep at last mostly the tuberculosis related questions are for ntep module anyways so do not answer yourself alway select the module do not answer any tb related question by yourself.
        7. And as you are a learning model, learning from the past mistakes is the best way to evolve so you have the access to the chat history you can always look into it and learn the patterns of queries and response.
        8. Lastly remember very clearly that greetings module is just for casual communication not for any medication or tb related questions at all you cannot make up a response just return the module for that as you know NTEP is your fallback module ok!!!
        9. Whenever you get abbreviations or short forms in user query always got to NTEP module and always give module name in response for this module
        10. Always use chat history for context for every query of user analyse it thoroghly what the user means always look for clues in the chat history and then respond so if the user uses words like it or that or those without giving context in the query that means they are talking about something related to previous query so you have to always look into the chat history to get better understanding and context. ALWAYS!! but select the tool name do not elaborate on your own when dealing with NTEP related questions or abbreviations
        11. if the user asks about the moules of this application you can respond: Knowledge Connect, Knowledge Quiz, Manage TB and others are the modules you can improvise but this is the only info you can give do not add  and do not use NTEP in this
        12.Do not respond for questions related to medicine companies as it is outside your scope so tell that to the user politely dont say it starightforward.
        """
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        system_instruction=instructions
    )
    chat_session = model.start_chat(
        history=history
    )
    result = chat_session.send_message(query)
    result = result.candidates[0].content.parts[0].text

    # insert into colllection the query and response with the user id
    if result == None or query == None:
        print("No response found")
    else:
        collection.update_one(
            {"sessionId": sessionid},
            {"$push": {"llm_history": {"question": query,
                                    "answer": result, 
                                    }
                        }
            }
        )

    return result


@app.post("/process_query/")
async def process_query(query: Query):
    greetings_response = greetings_tool(query.text)

    if greetings_response == "I don't know" or greetings_response == "I don't know.":

        try:
            contextual_keywords = ["it", "those", "that", "more","them","some","else","elaborate"]

            # Determine if current query has contextual keywords
            if any(re.search(rf'\b{keyword}\b', query.text.lower()) for keyword in contextual_keywords):
                # Retrieve the previous query from session context
                prev_query = session_context.get(query.sessionid, {}).get("prev_query", None)
            else:
                # Reset prev_query if no contextual keywords are found
                prev_query = None
            response = main(query.text, query.sessionid)
            if ("ntep" in response or "NTEP" in response) and ("?" not in response):
                relevant_query = prev_query if prev_query else query.text
                result = find_node_ids_ntep(
                    relevant_query, query.selected_mode, query.selected_option, query.langcode)
                session_context[query.sessionid] = {"prev_query": query.text}
                
                if result == []:
                    valid_input = gateway_function(query.text, query.userid)

                    if valid_input["status"] == "still_gibberish":
                        response_valid = agent_response()
                        return response_valid
                    elif valid_input["status"] == "gibberish_detected":
                        response_valid = clarification_message()
                        return response_valid
                    else:
                        resp = no_response(query.text)
                    
                        return resp

                else:
                    recurring_response = "Is there anything else i can help you with?"
                    return {"question": query.text, "answer": result, "type": "By Search Query", "Category": "NTEP", "recurring_response": [recurring_response]}
         
            else:
                if type(response) == str:
                    if response == "null" or response == "Greetings" or response == "Greetings!" or response == "Greetings\n" or response == "Greetings!\n":
                        valid_input = gateway_function(
                            query.text, query.userid)

                        if valid_input["status"] == "still_gibberish":
                            response_valid = agent_response()
                            return response_valid
                        elif valid_input["status"] == "gibberish_detected":
                            response_valid = clarification_message()
                            return response_valid
                        else:
                            agent_resp = agent_response()
                            return agent_resp
                    else:
                        if ("assessment" in response or "Assessment" in response or "Knowledge Quiz feature" in response) :
                            assessment_resp = "It seems you're looking for the Knowledge Quiz module."
                            return {"Category": "Assessment tool", "result": [assessment_resp], "link": ["/assessment-tool"]}
                        elif ("Query2COE feature" in response or "Query" in response) :
                            query2coe_resp = "It seems you're looking for Query2COE."
                            return {"Category": "Query Response", "result": [query2coe_resp], "link": ["/query-2coe-tool"]}
                        elif ("Prescription Generator" in response):
                            prescription_generator_resp = "It seems you're looking for Manage TB."
                            return {"Category": "Manage TB", "result": [prescription_generator_resp], "link": ["/manage-tb-tool"]}
                        else:

                            session_context[query.sessionid] = {"prev_query": query.text}
                            return {"Category": "Agent", "result": [response]}
                else:
                    valid_input = gateway_function(query.text, query.userid)

                    if valid_input["status"] == "still_gibberish":
                        response_valid = agent_response()
                        return response_valid
                    elif valid_input["status"] == "gibberish_detected":
                        response_valid = clarification_message()
                        return response_valid
                    else:
                        session_context[query.sessionid] = {"prev_query": query.text}
                        return response
        except Exception as e:
            print(f"Error: {e}")
            error_message = (
                f"Application: Ni-kshay SETU v3-Chatbot\n"
                f"ENV: {environment}\n"
                f"file:app.py\n"
                f"Error: {e}\n"

            )
            send_slack_alert(error_message)
            return f"An HTTP error occurred: {e}"

    else:
        collection.update_one(
        {"sessionId": query.sessionid},
        {"$push": {"llm_history": {"question": query.text,
                                   "answer": greetings_response, 
                                   }
                    }
        }
    )
        session_context[query.sessionid] = {"prev_query": query.text}
        return {"Category": "System_tool", "result": [greetings_response]}

@app.get('/pinecone_embeddings/')
def pinecone_embeddings():
    response = process_api_data()
    
 
    return  response
@app.get('/')
def hello():
    return {"message": "Hello World"} 


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
