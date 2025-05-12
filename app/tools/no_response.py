import random 

responses = ["I'm having trouble understanding your query. Could you please clarify or provide more details?",
"It seems I'm not sure what you're asking. Can you rephrase your question?",
"I didn’t catch that. Could you explain it in another way?",
"Sorry, I couldn’t process your request. Can you give me more information?",
"I’m not sure I understand. Could you ask your question differently?",
"I don't have a specific answer, but I can share general information about TB. Would you like to know more?",
"I’m unable to find an exact match, but I can provide general guidance on TB management. What would you like to learn about?",
"I couldn’t find that information, but I can tell you about TB symptoms or treatments. Which would you prefer?",
"It seems I don't have the details you need, but I can help with general TB-related topics. What would you like to discuss?",
"I can’t find an exact answer, but I can share some general knowledge about TB care. What are you interested in?",
"It looks like I might not have the information you're seeking. You can send us your query through the 'Contact Us' section, and someone will assist you.",
"I’m sorry, I couldn’t find that information. Please submit your query via the 'Contact Us' section, and our team will get back to you.",
"I’m unable to assist with that query. You can forward your question through our 'Contact Us' section, and we’ll connect you with an expert.",
"I don’t have the answer right now, but you can use the 'Contact Us' section to get in touch with a healthcare provider for further assistance.",
"It seems I'm out of my depth here. Please send us your query via the 'Contact Us' section, and we’ll ensure you get the help you need.",
"I’m sorry I couldn’t find the information. I’m continuously improving and will try to have an answer next time.",
"Apologies, I don’t have that information now. I’m learning every day and hope to have it soon.",
"I couldn’t find what you're looking for, but I’m always updating my knowledge. Please try again later.",
"I’m sorry I couldn’t assist with that query. I’m working on expanding my responses and will be better equipped next time.",
"Apologies for the inconvenience. I’m still learning, and I hope to provide you with the right information soon.",
"I don’t have an answer right now. Would you like me to record your query and follow up with you later?",
"I’m unable to find a response, but I can record your question and get back to you. Would that be okay?",
"I couldn’t locate the information. Should I log your query and notify you when I have an update?",
"I’m sorry I couldn’t help with that. Would you like me to record your query and get back to you?",
"It looks like I don’t have the details right now. I can record your question and reach out with the information later.",

]

agent_responses = ["I'm having trouble understanding your query. Could you please clarify or provide more details?",
"It seems I'm not sure what you're asking. Can you rephrase your question?",
"I didn’t catch that. Could you explain it in another way?",
"Sorry, I couldn’t process your request. Can you give me more information?",
"I’m not sure I understand. Could you ask your question differently?",]

clarification_messages = [
"I'm sorry if that wasn’t clear! Could you point out what’s confusing, so I can explain it better?",
"It looks like something didn’t make sense. Let me know where I lost you, and I'll rephrase it!",
"No problem! Let me walk you through this. What part would you like me to go over again?",
"I can totally explain that in more detail! Which part would you like me to focus on?",
"It seems like there’s some confusion. Could you share which part you’re unsure about, and I’ll break it down for you?",
"I’m here to help! What exactly would you like me to clarify?",
"Sorry about the confusion! Let me know which part is unclear, and I’ll do my best to simplify it.",
"That’s okay! Let’s take it step by step. What’s the part you’re not getting?",
"I see how that might be confusing! Can you tell me what’s unclear so I can assist further?",
"It sounds like something isn’t clicking. What can I clarify for you?",
"I understand if this is tricky! Where can I provide more details to help?",
"Let’s go over this again. What part didn’t make sense to you?",
"Sorry if it’s a bit confusing! Could you let me know what part I should explain in more detail?",
"Don’t worry if you’re not following. I’m happy to help clarify! What’s unclear to you right now?",
"I can see why that might be confusing. Let me know what you need more help with!",
"No problem! What exactly would you like me to go over again?",
"It’s totally fine not to get it right away! Tell me what part you’d like me to explain again.",
"Sorry if that was confusing! Let’s try a different approach. What’s unclear?",
"Thanks for your patience! Could you let me know which part wasn’t clear so I can help?",
"It’s okay! I’m here to explain things as many times as needed. What’s confusing for you?",
"That’s alright! I’m here to help. Could you tell me what part you need more details on?",
"I get that this can be a bit tricky. Let’s figure it out together—what’s not making sense?",
"Don’t worry! Let me know where I can explain things better for you.",
"Sorry if this wasn’t clear! Where can I add more detail to help you understand better?",
"I’m here to clarify any confusion! What specifically would you like me to explain further"
]


def clarification_message():
    clarification_msg = random.choice(clarification_messages)
    return {"Category": 'Agent', "result": [clarification_msg]}

def no_response(query):
  
    # Select a random response from the list
    resp = random.choice(responses)
    return {"question":query, "anwser": [resp],"type":"By Search Query","Category": "NTEP"}

def agent_response():
    agent_resp = random.choice(agent_responses)
    return {"Category": 'Agent', "result": [agent_resp]}