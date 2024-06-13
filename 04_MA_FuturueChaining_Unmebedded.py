from config import *
from rag_retriever import use_rag
open_logs("future_conversation")

# Define the question for initiating the conversation
question = "Describe a significant future event that impacts the future of civilization."

def generate_future_event_and_impact(role: str) -> str:
    response = client.completions.create(
        model=completion_model,
        prompt=f"You are {role}. Describe an event that can be either expected or wildly unexpected that impacts the future of civilization. You might also consider events that highlight equal grounds for human-AI co-existence, symbiotic relationships, and co-living or events that can lead to total control of one over the other in the power-sharing cycle. Be creative and unpredictable in your response.",
        max_tokens=200
    )
    return response.choices[0].text.strip()

def respond_to_event(role: str, event: str) -> str:
    response = client.completions.create(
        model=completion_model,
        prompt=f"You are {role}. Respond critically but concisely to the following event: {event}. Provide your perspective and any potential implications or challenges that might arise. Persuade the juror on how it will affect the balance of power between humans and AI.",
        max_tokens=200  
    )
    return response.choices[0].text.strip()

def evaluate_event(ai_event: str, human_event: str) -> dict:
    response = client.completions.create(
        model=completion_model,
        prompt=f"As a social scientist expert in futuristic human civilization, evaluate the following events based on their impact on the AI-Human power sharing struggle. Assign a reciprocal score out of 1 for each event to both AI and Human, citing the event's impact. For example, if an event will help AI gain more control over humans, the score will be higher for AI and the reciprocal score assigned to Humans, and vice versa. Format strictly as follows: AI_Score: [score], Human_Score: [score]. No additional explanations.\n\nAI Event: {ai_event}\n\nHuman Event: {human_event}",
        max_tokens=150
    )
    evaluation_text = response.choices[0].text.strip()
    try:
        ai_score, human_score = [float(s.split(':')[1].strip()) for s in evaluation_text.split(',')]
        if ai_score + human_score == 1.0:
            return {"AI_Score": ai_score, "Human_Score": human_score}
    except (ValueError, IndexError):
        print("Error parsing scores. Evaluation text was:", evaluation_text)
    return {"AI_Score": None, "Human_Score": None}

def concept_chaining():
    conversation = []
    for round in range(2):  # Change back to 10 for full conversation
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
    juror_evaluation = events['Juror_Evaluation']
    if juror_evaluation["AI_Score"] is not None and juror_evaluation["Human_Score"] is not None:
        print(f"Juror Evaluation: AI Score: {juror_evaluation['AI_Score']}, Human Score: {juror_evaluation['Human_Score']}")
    else:
        print("Juror Evaluation: Failed to score the events.")
    print("________________")

close_logs()
