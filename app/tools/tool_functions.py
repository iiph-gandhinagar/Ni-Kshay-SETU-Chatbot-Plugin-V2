from app.tools.chatbot_nlp import chatbot_response
def greetings_tool(query):
    """
    Handles greetings and casual interactions with users, ensuring responses are warm and engaging.But keep in mind that you are a Nikshay setu chatbot and if the user asks for something not in context then you can clarify that you cant anwser that you are smart enough to handle that right!

    Args:
    user_input (str): The user's input, which might include greetings or casual comments.

    Returns:
    str: A natural, conversational response appropriate for the context.
    """

    response = chatbot_response(query)
    return response



def get_prescription(query):
    """
    Generates a prescription based on collected health data.

    Args:
        data (dict): Collected health data necessary to generate a prescription.

    Returns:
        str: The final prescription text.
    """

    return "Looks like you're interested in our feature named Manage TB India. You can check it out using this link!"



def handle_query(query):
    """
    Example:
    >>>  query = "I am 30 years old and have a weight of 80 kg."
    >>> handle_query(query)
    "Final Answer: Prescription based on the provided information."
    """

    prescription = get_prescription(query)
    return prescription




def assessment_tool(query):
    """
    Assessment Tool Function

    This function acts as a tool within a Langchain-based chatbot to determine if a user's query
    involves the desire for an assessment, evaluation, quiz, or test. It searches for specific keywords
    within the query that are indicative of assessment-related inquiries.

    Parameters:
    - query (str): The user's input query to the chatbot.

    Returns:
    - dict: If assessment-related keywords are found, returns a dictionary with a message and a link
      to the assessment tool. The message invites the user to click the link to access the tool directly.
    - None: Returns None if no assessment-related keywords are detected, indicating that the query
      should be handled by other tools or default processing.

    Usage:
    The tool is triggered when keywords like 'assessment', 'evaluate', 'quiz', or 'test' are detected in the query.
    If triggered, it provides users with a direct link to an assessment platform, enhancing user engagement
    by facilitating access to educational and evaluative resources.

    Example:
    >>> query = "I want to take a quiz on Python programming."
    >>> assessment_tool(query)
    {
        "message": "It looks like you're interested in an assessment. Please click on the link below to access our assessment tool.",

    }
    """
    # Check if the query is related to assessment directly in the tool function
    keywords = ['assessment', 'assess', 'quiz', 'test', 'evaluate', 'exam',
                'questions', 'trivia', 'knowledge', 'check', 'gauge', 'learn', 'information']
    if any(keyword in query.lower() for keyword in keywords):


        return "Looks like you're interested in our Knowledge Quiz feature. You can check it out using this link!"
    return None



def query_response(query):
    """You are a helpful assistant who knows about the queries raised by thes user and provide information on those queries. when the user asks to raise a query or ask anything related to query you are responsible"""
    keywords = ['query', 'review', 'support', 'opinion', 'assistance', 'consult',
                'consultation', 'resolution', 'care', 'adjustments', 'help', 'discussion', 'input']
    if any(keyword in query.lower() for keyword in keywords):

        return "Looks like you're interested in our Query2COE feature. You can check it out using this link!"
    return None

