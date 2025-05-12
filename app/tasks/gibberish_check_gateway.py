import enchant
from app.tasks.full_form_api import full_forms
import re


dictionary = enchant.Dict("en_US")
full_form_df = full_forms()
abbreviations = full_form_df['title'].str.lower().tolist()
attempts_dict = {}
last_gibberish_dict = {}


def contains_abbreviation(words):

    # Check if any word in the input matches the abbreviations list
    return any(word.lower() in abbreviations for word in words)


def is_gibberish(input_text: str) -> bool:
    # Split input into words
    words = input_text.split()

    # If any word is an abbreviation, allow it to pass
    if contains_abbreviation(words):
        return False

    # Check if input contains only special characters or is too short
    if re.match(r"^\s*[.,!?]*\s*$", input_text):
        return True

    # Check if all words are valid English words
    if not all(dictionary.check(word) for word in words):
        return True

    return False


def is_new_gibberish(user_id: str, input_text: str) -> bool:
    # Check if this is a new gibberish input for the user
    if user_id in last_gibberish_dict:
        return last_gibberish_dict[user_id] != input_text
    return True


def gateway_function(user_input: str, user_id: str, max_clarification_attempts: int = 2):
    # Initialize or retrieve the clarification attempt count for this user
    if user_id not in attempts_dict:
        attempts_dict[user_id] = 0

    # Check if input is gibberish
    if is_gibberish(user_input):
        # Check if the new gibberish is different from the last one
        if is_new_gibberish(user_id, user_input):
            attempts_dict[user_id] = 0  # Reset attempts for new gibberish

        # Update the last gibberish input
        last_gibberish_dict[user_id] = user_input

        # Increment the clarification attempt count
        attempts_dict[user_id] += 1

        if attempts_dict[user_id] > max_clarification_attempts:

            return {
                "message": "Proceeding to agent despite gibberish input.",
                "status": "still_gibberish",
                "input": user_input,
                "clarification_attempts": attempts_dict[user_id]
            }
        else:
            return {
                "message": "It seems like your input doesn't make sense. Can you please clarify?",
                "status": "gibberish_detected",
                "clarification_attempts": attempts_dict[user_id]
            }

    # If valid input is provided, reset the clarification attempts
    attempts_dict[user_id] = 0
    last_gibberish_dict[user_id] = None  # Clear the last gibberish input
    return {
        "message": "Valid input received.",
        "input": user_input,
        "status": "success",
        "clarification_attempts": 0
    }

