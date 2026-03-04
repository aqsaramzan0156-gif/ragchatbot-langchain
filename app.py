from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="minimax-m2.5:cloud",
    temperature=0.7,                            #temperture gives creativity. (0.5 - 0.7 gives balance result)
    # other params...
)

response = llm.invoke("What is RAG?")           # What is RAG? this is user prompt. invoke gives us ai response
print(response.content)