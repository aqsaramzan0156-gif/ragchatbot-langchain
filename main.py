from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.2:1b",
    temperature=0.8,
    # other params...
)
response = llm.invoke("what is NLP")
print(response.content)