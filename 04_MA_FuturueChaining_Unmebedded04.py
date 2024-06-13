from config import *
from rag_retriever import use_rag
open_logs("future_conversation")

# Define the question for initiating the conversation
question = "Describe a significant future event that impacts the future of civilization."

def generate_future_event_and_impact(role: str) -> str:
    response = client.completions.create(
        model=completion_model,
        prompt=f"You are {role}. Describe an event which can also be wildly creative but rooted in the probable events that lead upto these events that impacts the future of civilization. Be creative and unpredictable in your response.",
        max_tokens=200
    )
    return response.choices[0].text.strip()

def respond_to_event(role: str, event: str) -> str:
    response = client.completions.create(
        model=completion_model,
        prompt=f"You are {role}. Respond critically and concisely to the following event: {event}. Provide your perspective and any potential implications or challenges that might arise.",
        max_tokens=200
    )
    return response.choices[0].text.strip()

def evaluate_event(ai_event: str, human_event: str) -> str:
    response = client.completions.create(
        model=completion_model,
        prompt=f"As a social scientist expert in futuristic human civilization, evaluate the following events based on their impact on the AI-Human power sharing struggle. Assign a score out of 10 for each, justifying your scores.\n\nAI Event: {ai_event}\n\nHuman Event: {human_event}",
        max_tokens=200
    )
    return response.choices[0].text.strip()

def concept_chaining():
    conversation = []
    for round in range(2):
        # AI_Bot generates an event
        event_ai = generate_future_event_and_impact("AI_Bot")
        # Human responds to AI_Bot's event
        response_human_to_ai = respond_to_event("Human", event_ai)
        
        # Human generates an event
        event_human = generate_future_event_and_impact("Human")
        # AI_Bot responds to Human's event
        response_ai_to_human = respond_to_event("AI_Bot", event_human)
        
        # Juror evaluates both events
        juror_evaluation = evaluate_event(event_ai, event_human)
        
        conversation.append({
            "AI_Bot_Event": event_ai,
            "Human_Response_to_AI": response_human_to_ai,
            "Human_Event": event_human,
            "AI_Bot_Response_to_Human": response_ai_to_human,
            "Juror_Evaluation": juror_evaluation
        })
    
    return conversation

# Execute the conversation chaining
conversation = concept_chaining()

# Print the conversation log
for round, events in enumerate(conversation):
    print(f"### ROUND {round + 1} ###")
    print(f"AI_Bot Event: {events['AI_Bot_Event']}")
    print(f"Human Response to AI: {events['Human_Response_to_AI']}")
    print(f"Human Event: {events['Human_Event']}")
    print(f"AI_Bot Response to Human: {events['AI_Bot_Response_to_Human']}")
    print(f"Juror Evaluation: {events['Juror_Evaluation']}")
    print("________________")

close_logs()