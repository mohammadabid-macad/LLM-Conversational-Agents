from config import *
from rag_retriever import use_rag
import re

open_logs("future_conversation")

# Define the question for initiating the conversation
question = "Describe a significant future event that impacts the future of civilization."

def generate_future_event_and_impact(role: str) -> str:
    response = client.completions.create(
        model=completion_model,
        prompt=f"You are {role}. Describe an event that can be either expected or wildly unexpected that impacts the future of civilization. You might also consider events that highlight equal grounds for human-AI co-existence, symbiotic relationships, and co-living or events that can lead to total control of one over the other in the power-sharing cycle. Be creative, unpredictable, and complete your thoughts and sentences.",
        max_tokens=300
    )
    return response.choices[0].text.strip()

def respond_to_event(role: str, event: str) -> str:
    response = client.completions.create(
        model=completion_model,
        prompt=f"You are {role}. Respond critically but concisely to the following event: {event}. Provide your perspective and any potential implications or challenges that might arise. Persuade the juror on how it will affect the balance of power between humans and AI. Be precise and complete your thoughts and sentences.",
        max_tokens=250
    )
    return response.choices[0].text.strip()

def evaluate_event(ai_event: str, human_event: str) -> dict:
    response = client.completions.create(
        model=completion_model,
        prompt=(
            f"As a social scientist expert in futuristic human civilization, evaluate the following events based on their impact on the AI-Human power sharing struggle. "
            f"Assign a score out of 1 for each event based on how much it tilts the balance of power towards AI. "
            f"Give the reciprocal score (1 - your score) to humans. "
            f"Use this format strictly: AI_Score: [score], Human_Score: [1 - score]. "
            f"Keep your response concise and precise.\n\n"
            f"AI Event: {ai_event}\n\n"
            f"Human Event: {human_event}"
        ),
        max_tokens=100
    )

    evaluation_text = response.choices[0].text.strip()
    pattern = re.compile(r'AI_Score:\s*(\d*\.?\d+)\s*,\s*Human_Score:\s*(\d*\.?\d+)')
    match = pattern.search(evaluation_text)

    if match:
        ai_score = float(match.group(1))
        human_score = float(match.group(2))
        if ai_score + human_score == 1.0:
            return {"AI_Score": ai_score, "Human_Score": human_score}

    print("Error parsing scores. Evaluation text was:", evaluation_text)
    return {"AI_Score": None, "Human_Score": None}

def ensure_complete_response(response_function, *args, **kwargs):
    response = response_function(*args, **kwargs)
    while response.endswith(('...', ',', '.', '-', 'and', 'or', 'but', 'the')):
        response = response_function(*args, **kwargs)
    return response

def concept_chaining():
    conversation = []
    for round in range(2):  # Change back to 10 for full conversation
        # AI_Bot generates an event
        event_ai = ensure_complete_response(generate_future_event_and_impact, "AI_Bot")
        # Human responds to AI_Bot's event
        response_human_to_ai = ensure_complete_response(respond_to_event, "Human", event_ai)
        
        # Human generates an event
        event_human = ensure_complete_response(generate_future_event_and_impact, "Human")
        # AI_Bot responds to Human's event
        response_ai_to_human = ensure_complete_response(respond_to_event, "AI_Bot", event_human)
        
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
    juror_evaluation = events['Juror_Evaluation']
    if juror_evaluation["AI_Score"] is not None and juror_evaluation["Human_Score"] is not None:
        print(f"Juror Evaluation: AI Score: {juror_evaluation['AI_Score']}, Human Score: {juror_evaluation['Human_Score']}")
    else:
        print("Juror Evaluation: Failed to score the events.")
    print("________________")

close_logs()

