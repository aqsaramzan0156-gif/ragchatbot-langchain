from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

MAX_TURNS = int(os.getenv("MAX_TURNS", "5" ))
MODEL_NAME = os.getenv("MODEL_NAME", "minimax-m2.5:cloud")
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.5))

load_dotenv()
llm = ChatOllama(
    model=MODEL_NAME,
    temperature=TEMPERATURE,                                                            # temperature gives creativity (0.5 - 0.7 gives balanced results)
)

# Making chat prompt 
prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="You are a helpful AI assistance."),
    MessagesPlaceholder(variable_name="chat_history"),
    HumanMessage(content="{question}")  
])

chain = prompt | llm | StrOutputParser()  # "|" combines multiple components

chat_history = []  # This empty list will store the conversation history
#MAX_TURNS = 4        # 10 exchanges = 20 messages (question + response -> human + ai)

def chat(question):
    current_turns = len(chat_history) / 2
    if current_turns >= MAX_TURNS:
        return (
            "Context window is full. "
            "The AI may not follow your previous thread properly. "
            "Please type 'clear' for new chat"
        )

    response = chain.invoke({
        "question": question,
        "chat_history": chat_history
    })
    
    # Add to chat history
    chat_history.append(HumanMessage(content=question))
    chat_history.append(AIMessage(content=response))
    
    # this will message when 80% of our context window is full 
    remaining = MAX_TURNS - (current_turns + 1)
    if remaining <= 2:
        response += f"\n[System: You have {remaining} turn(s) left before context window fills]"
    
    return response  # Return the response so it can be printed

def main():
    print("Langchain chatbot ready! (Type 'quit' for exit, 'clear' to reset the history)")
    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue
        if user_input.lower() == "quit":
            break
        if user_input.lower() == "clear":
            chat_history.clear()
            print("History cleared")
            continue  # Skip to next iteration after clearing
        
        # Fixed indentation: This line was outside the while loop
        print(f"AI: {chat(user_input)}\n")

if __name__ == "__main__":
    main()