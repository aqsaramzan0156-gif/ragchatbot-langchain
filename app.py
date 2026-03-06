from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
import streamlit as st
import tiktoken

# ── LLM setup ──
llm = ChatOllama(
    model="minimax-m2.5:cloud",
    temperature=0.7,
)

# ── Prompt template ──
prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="You are a helpful AI assistant."),
    MessagesPlaceholder(variable_name="chat_history"),
    HumanMessage(content="{question}")
])

chain = prompt | llm | StrOutputParser()

# ── Token settings ──
MAX_TOKENS = 2000       # max tokens allowed in chat history
WARN_AT    = 0.80       # warn user when 80% of token budget is used

# ── Token counting using tiktoken ──
def count_tokens(text: str) -> int:
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))

def count_history_tokens(history: list) -> int:
    return sum(count_tokens(msg.content) for msg in history)

def trim_history(history: list, new_question: str) -> list:
    """Remove oldest message pairs until history + new question fits in MAX_TOKENS."""
    while history:
        used = count_history_tokens(history) + count_tokens(new_question)
        if used <= MAX_TOKENS:
            break
        if len(history) >= 2:
            history = history[2:]   # remove oldest human + ai pair
        else:
            history = []
    return history

# ── Session state ──
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ── Streamlit UI ──
st.title("AI Chatbot")
st.caption("Context window managed by token count · Powered by Ollama")

# ── Sidebar ──
with st.sidebar:
    st.header("Settings")
    used_tokens = count_history_tokens(st.session_state.chat_history)
    st.metric("Tokens Used", f"{used_tokens} / {MAX_TOKENS}")
    st.progress(min(used_tokens / MAX_TOKENS, 1.0))

    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

# ── Display chat history ──
for msg in st.session_state.chat_history:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.write(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.write(msg.content)

# ── Chat input ──
if question := st.chat_input("Ask me anything..."):

    # Trim history to fit within token budget
    st.session_state.chat_history = trim_history(st.session_state.chat_history, question)

    # Warn if context is getting full
    used = count_history_tokens(st.session_state.chat_history)
    if used / MAX_TOKENS >= WARN_AT:
        st.warning(f"Context window is {used/MAX_TOKENS*100:.0f}% full. Older messages may be removed soon.")

    # Show user message
    with st.chat_message("user"):
        st.write(question)

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chain.invoke({
                "question": question,
                "chat_history": st.session_state.chat_history
            })
        st.write(response)

    # Update chat history
    st.session_state.chat_history.append(HumanMessage(content=question))
    st.session_state.chat_history.append(AIMessage(content=response))

    st.rerun()