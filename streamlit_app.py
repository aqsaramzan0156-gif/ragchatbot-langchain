"""
Streamlit Web UI for AI Chatbot
Professional, modern interface with header, sidebar, and chat functionality
"""
import streamlit as st
import sys
import os
from datetime import datetime

# Import from existing app.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Page configuration
st.set_page_config(
    page_title="AI Assistant",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    /* Global Styles */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: #0d1117;
        min-height: 100vh;
    }

    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    header {visibility: hidden !important;}

    /* Main container */
    .main-content {
        max-width: 900px;
        margin: 0 auto;
        padding: 0 20px;
    }

    /* Custom Header */
    .custom-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 25px 30px;
        border-radius: 16px;
        margin-bottom: 24px;
        border: 1px solid rgba(99, 102, 241, 0.2);
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3);
    }
    .custom-header h1 {
        color: #ffffff;
        margin: 0;
        font-size: 1.8rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .custom-header p {
        color: rgba(255,255,255,0.6);
        margin: 8px 0 0 0;
        font-size: 0.9rem;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: #0d1117 !important;
        border-right: 1px solid rgba(255,255,255,0.06);
    }
    .sidebar-section {
        background: rgba(255,255,255,0.03);
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 16px;
        border: 1px solid rgba(255,255,255,0.06);
    }
    .sidebar-title {
        color: #e2e8f0;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Chat Container */
    .chat-container {
        background: #161b22;
        border-radius: 16px;
        padding: 24px;
        border: 1px solid rgba(255,255,255,0.06);
        min-height: 450px;
        max-height: 65vh;
        overflow-y: auto;
    }

    /* Message Bubbles */
    .message-wrapper {
        display: flex;
        margin-bottom: 16px;
        animation: fadeIn 0.3s ease;
    }
    .message-wrapper.user {
        justify-content: flex-end;
    }
    .message-wrapper.assistant {
        justify-content: flex-start;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .message-avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
        flex-shrink: 0;
    }
    .user .message-avatar {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        margin-left: 12px;
    }
    .assistant .message-avatar {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        margin-right: 12px;
    }

    .message-bubble {
        max-width: 75%;
        padding: 14px 18px;
        border-radius: 16px;
        line-height: 1.6;
        font-size: 0.95rem;
    }
    .user .message-bubble {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border-bottom-right-radius: 4px;
        box-shadow: 0 2px 12px rgba(99, 102, 241, 0.3);
    }
    .assistant .message-bubble {
        background: #21262d;
        color: #e6edf3;
        border: 1px solid rgba(255,255,255,0.08);
        border-bottom-left-radius: 4px;
    }

    .message-time {
        font-size: 0.7rem;
        color: rgba(255,255,255,0.4);
        margin-top: 6px;
    }

    /* Input Area */
    .input-wrapper {
        background: #161b22;
        border-radius: 16px;
        padding: 16px;
        border: 1px solid rgba(255,255,255,0.08);
        margin-top: 20px;
        transition: all 0.3s ease;
    }
    .input-wrapper:focus-within {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
    }

    /* Status Cards */
    .status-card {
        background: rgba(255,255,255,0.03);
        border-radius: 10px;
        padding: 14px 16px;
        border: 1px solid rgba(255,255,255,0.06);
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #10b981;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    /* Progress Bar */
    .progress-container {
        background: rgba(255,255,255,0.08);
        border-radius: 8px;
        height: 6px;
        overflow: hidden;
        margin-top: 8px;
    }
    .progress-bar {
        height: 100%;
        border-radius: 8px;
        background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
        transition: width 0.5s ease;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 500;
        font-size: 0.9rem;
        transition: all 0.2s ease;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.4);
    }

    /* Quick Action Buttons */
    .action-btn {
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.3);
        color: #a5b4fc;
        padding: 8px 14px;
        border-radius: 8px;
        font-size: 0.85rem;
        cursor: pointer;
        transition: all 0.2s ease;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    .action-btn:hover {
        background: rgba(99, 102, 241, 0.25);
        border-color: rgba(99, 102, 241, 0.5);
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 24px;
        color: rgba(255,255,255,0.35);
        font-size: 0.8rem;
        border-top: 1px solid rgba(255,255,255,0.06);
        margin-top: 24px;
    }

    /* Empty State */
    .empty-state {
        text-align: center;
        padding: 60px 20px;
        color: rgba(255,255,255,0.4);
    }
    .empty-state-icon {
        font-size: 3rem;
        margin-bottom: 16px;
        opacity: 0.5;
    }
    .empty-state h3 {
        color: rgba(255,255,255,0.6);
        font-weight: 500;
        margin-bottom: 8px;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(255,255,255,0.15);
        border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255,255,255,0.25);
    }

    /* Markdown in messages */
    .assistant .message-bubble p {
        margin: 0 0 8px 0;
    }
    .assistant .message-bubble p:last-child {
        margin-bottom: 0;
    }
    .assistant .message-bubble code {
        background: rgba(255,255,255,0.1);
        padding: 2px 6px;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85em;
    }
    .assistant .message-bubble pre {
        background: #0d1117;
        padding: 12px;
        border-radius: 8px;
        overflow-x: auto;
        margin: 10px 0;
    }
    .assistant .message-bubble pre code {
        background: transparent;
        padding: 0;
    }

    /* Info boxes */
    .info-box {
        background: rgba(99, 102, 241, 0.1);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 8px;
        padding: 12px 16px;
        margin: 10px 0;
        font-size: 0.85rem;
        color: #a5b4fc;
    }

    /* Text Input */
    .stTextInput > div > div > input {
        background: transparent !important;
        border: none !important;
        color: #e6edf3 !important;
        font-size: 1rem !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: rgba(255,255,255,0.3) !important;
    }

    /* Warning messages */
    .warning-badge {
        background: rgba(245, 158, 11, 0.15);
        border: 1px solid rgba(245, 158, 11, 0.3);
        color: #fbbf24;
        padding: 6px 12px;
        border-radius: 6px;
        font-size: 0.8rem;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        margin-top: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Import app configuration
from app import MAX_TURNS

# Session state initialization
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    # Logo/Branding
    st.markdown("""
    <div style="text-align: center; padding: 10px 0 20px 0;">
        <div style="font-size: 2.5rem; margin-bottom: 8px;">✨</div>
        <div style="font-size: 1.1rem; font-weight: 600; color: #e2e8f0;">AI Assistant</div>
        <div style="font-size: 0.75rem; color: rgba(255,255,255,0.4);">LangChain + Ollama</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Model Info
    st.markdown("""
    <div class="sidebar-title">
        <span>⚡</span> Model Configuration
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="status-card">
        <span style="color: rgba(255,255,255,0.6);">Model</span>
        <span style="color: #10b981; font-weight: 500;">minimax-m2.5</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 12px;">
        <div class="status-card">
            <span style="color: rgba(255,255,255,0.6); font-size: 0.8rem;">Temperature</span>
            <span style="color: #a5b4fc; font-weight: 500;">0.7</span>
        </div>
        <div class="status-card">
            <span style="color: rgba(255,255,255,0.6); font-size: 0.8rem;">Max Turns</span>
            <span style="color: #a5b4fc; font-weight: 500;">{}</span>
        </div>
    </div>
    """.format(MAX_TURNS), unsafe_allow_html=True)

    st.markdown("---")

    # Context Usage
    st.markdown("""
    <div class="sidebar-title">
        <span>📊</span> Context Usage
    </div>
    """, unsafe_allow_html=True)

    # Get chat history count from app.py
    try:
        from app import chat_history as app_chat_history
        current_turns = len(app_chat_history) / 2
    except:
        current_turns = 0

    progress_percent = min((current_turns / MAX_TURNS) * 100, 100)
    remaining = MAX_TURNS - current_turns

    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-bar" style="width: {progress_percent}%"></div>
    </div>
    <div style="display: flex; justify-content: space-between; margin-top: 8px; font-size: 0.8rem; color: rgba(255,255,255,0.5);">
        <span>{int(current_turns)} / {MAX_TURNS} turns</span>
        <span>{int(100 - progress_percent)}% left</span>
    </div>
    """, unsafe_allow_html=True)

    if remaining <= 2:
        st.markdown(f"""
        <div class="warning-badge" style="margin-top: 12px;">
            ⚠️ Only {int(remaining)} turn(s) left
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Quick Actions
    st.markdown("""
    <div class="sidebar-title">
        <span>🎯</span> Quick Actions
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            try:
                from app import chat_history as app_chat_history
                app_chat_history.clear()
            except:
                pass
            st.rerun()

    with col2:
        if st.button("💾 Save Chat", use_container_width=True):
            if st.session_state.messages:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"chat_history_{timestamp}.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("=" * 50 + "\\n")
                    f.write(f"Chat History - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n")
                    f.write("=" * 50 + "\\n\\n")
                    for msg in st.session_state.messages:
                        f.write(f"[{msg['role'].upper()}]\\n{msg['content']}\\n\\n")
                st.success(f"✅ Saved to {filename}")
            else:
                st.info("No chat to save")

    st.markdown("---")

    # Keyboard Shortcuts
    st.markdown("""
    <div class="sidebar-title">
        <span>⌨️</span> Shortcuts
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size: 0.8rem; color: rgba(255,255,255,0.5); line-height: 1.8;">
        <div><kbd style="background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px;">Enter</kbd> Send message</div>
        <div><kbd style="background: rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 4px;">Shift+Enter</kbd> New line</div>
    </div>
    """, unsafe_allow_html=True)

# Main content
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Header
st.markdown("""
<div class="custom-header">
    <h1>✨ AI Assistant</h1>
    <p>Powered by LangChain + Ollama • Start a conversation</p>
</div>
""", unsafe_allow_html=True)

# Status bar
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.markdown("""
    <div class="status-card" style="padding: 10px 14px;">
        <div class="status-dot"></div>
        <span style="color: #10b981; font-weight: 500;">Online</span>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="status-card" style="padding: 10px 14px;">
        <span style="color: rgba(255,255,255,0.6);">Messages</span>
        <span style="color: #e2e8f0; font-weight: 500;">{len(st.session_state.messages)}</span>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown(f"""
    <div class="status-card" style="padding: 10px 14px;">
        <span style="color: rgba(255,255,255,0.6);">Remaining</span>
        <span style="color: #a5b4fc; font-weight: 500;">{int(remaining)} turns</span>
    </div>
    """, unsafe_allow_html=True)

# Chat container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display messages or empty state
if not st.session_state.messages:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-state-icon">💬</div>
        <h3>Start a conversation</h3>
        <p>Send a message to begin chatting with the AI</p>
    </div>
    """, unsafe_allow_html=True)
else:
    for i, message in enumerate(st.session_state.messages):
        timestamp = datetime.now().strftime("%H:%M")

        if message["role"] == "user":
            st.markdown(f"""
            <div class="message-wrapper user">
                <div class="message-bubble">
                    {message["content"]}
                    <div class="message-time">{timestamp}</div>
                </div>
                <div class="message-avatar">👤</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="message-wrapper assistant">
                <div class="message-avatar">✨</div>
                <div class="message-bubble">
                    {message["content"]}
                    <div class="message-time">{timestamp}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Input area
st.markdown('<div class="input-wrapper">', unsafe_allow_html=True)

with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([6, 1])
    with col1:
        user_input = st.text_input(
            "Type your message...",
            placeholder="Ask me anything...",
            label_visibility="collapsed",
            key="chat_input"
        )
    with col2:
        submit_button = st.form_submit_button(
            "Send",
            use_container_width=True
        )

if submit_button and user_input.strip():
    # Add user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Get AI response
    try:
        from app import chat_history as app_chat_history, chain

        # Check context window
        current_turns = len(app_chat_history) / 2

        if current_turns >= MAX_TURNS:
            response = (
                "⚠️ **Context window is full.**\n\n"
                "The conversation history has reached its limit. "
                "Please click **Clear Chat** in the sidebar to start fresh."
            )
        else:
            # Get response using the chain from app.py
            from langchain_core.messages import HumanMessage, AIMessage

            response = chain.invoke({
                "question": user_input,
                "chat_history": app_chat_history
            })

            # Add to chat history
            app_chat_history.append(HumanMessage(content=user_input))
            app_chat_history.append(AIMessage(content=response))

            # Add warning if low on turns
            remaining = MAX_TURNS - (current_turns + 1)
            if remaining <= 2:
                response += f"\n\n📝 *You have {remaining} turn(s) left before the context window fills.*"

        # Add AI response
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"⚠️ An error occurred: {str(e)}"
        })

    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown(f"""
<div class="footer">
    <p>✨ AI Assistant • Built with Streamlit & LangChain</p>
    <p style="font-size: 0.75rem; opacity: 0.6;">Context Window: {MAX_TURNS} turns • Temperature: 0.7</p>
</div>
""", unsafe_allow_html=True)
