from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(
    model="minimax-m2.5:cloud",
    temperature=0.7,                            #temperture gives creativity. (0.5 - 0.7 gives balance result                                                      
)


    # making chat prompt

prompt =ChatPromptTemplate.from_messages([
    SystemMessage(content="You are a helpful AI assistance."),
    HumanMessage(content="what is RAG?")
])

chain = prompt | llm | StrOutputParser()            # "|" we used this to combine multiple things

response = chain.invoke({"question": "What is RAG?"})           # What is RAG? this is user prompt. invoke gives us ai response
print(response)
for chunk in chain.stream({"question": "Whar is NLP?"}):
    print(chunk, end= "", flush = True)