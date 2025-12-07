import streamlit as st
import requests
import time
from datetime import datetime
from dotenv import load_dotenv
import os
from icecream import ic

load_dotenv()

# FastAPI backend URL
API_URL = os.getenv("API_URL")
# Page configuration
st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# # Custom CSS for better styling
# st.markdown("""
#     <style>
#     .main {
#         padding: 0rem 1rem;
#     }
#     .stTextInput > div > div > input {
#         border-radius: 20px;
#     }
#     .chat-message {
#         padding: 1.5rem;
#         border-radius: 15px;
#         margin-bottom: 1rem;
#         display: flex;
#         flex-direction: column;
#     }
#     .user-message {
#         background-color: #e3f2fd;
#         margin-left: 20%;
#     }
#     .assistant-message {
#         background-color: #f5f5f5;
#         margin-right: 20%;
#     }
#     .message-header {
#         font-weight: bold;
#         margin-bottom: 0.5rem;
#         display: flex;
#         align-items: center;
#         gap: 0.5rem;
#     }
#     .message-content {
#         margin-left: 2rem;
#     }
#     .timestamp {
#         font-size: 0.8rem;
#         color: #666;
#         margin-top: 0.5rem;
#     }
#     .stButton > button {
#         border-radius: 20px;
#         padding: 0.5rem 2rem;
#     }
#     </style>
# """, unsafe_allow_html=True)


# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }

    .stTextInput > div > div > input {
        border-radius: 20px;
    }

    .chat-message {
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }

    /* ✅ USER MESSAGE → GREEN with BLACK TEXT */
    .user-message {
    background-color: #d1fae5;   /* soft green */
    border-left: 5px solid #10b981;
    margin-left: 20%;
    color: #000000;              /* ✅ BLACK TEXT */
}

   .assistant-message {
    background-color: #ede9fe;
    border-left: 5px solid #7c3aed;
    margin-right: 20%;
    color: #1f2937;
}


    .message-header {
        font-weight: bold;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .message-content {
        margin-left: 2rem;
    }

    .timestamp {
        font-size: 0.8rem;
        color: #666;
        margin-top: 0.5rem;
    }

    .stButton > button {
        border-radius: 20px;
        padding: 0.5rem 2rem;
    }
    </style>
""", unsafe_allow_html=True)


# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_count" not in st.session_state:
    st.session_state.chat_count = 0

if "enter_pressed" not in st.session_state:
    st.session_state.enter_pressed = False


if "my_text" not in st.session_state:
    st.session_state.my_text = ""


def submit():
    st.session_state.my_text = st.session_state.widget
    st.session_state.widget = ""
    st.session_state.enter_pressed = True  # ← Added this

# Sidebar
with st.sidebar:
    # st.title("VenkyAI")
    st.markdown("---")
    
    st.markdown("### 💡 About")
    st.info(
        "This is an AI-powered chat assistant that uses advanced "
        "language models to help answer your questions and engage "
        "in meaningful conversations."
    )
    
    st.metric("Total Messages", len(st.session_state.messages))
    # st.metric("Conversations", st.session_state.chat_count)
    
    st.markdown("---")
    
    if st.button("🗑️ Clear Previous Chat ", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_count += 1
        st.rerun()
    
    # st.markdown("---")
    # st.markdown("### ⚙️ Settings")
    # api_status = st.empty()
    
    # # Check API health
    # try:
    #     health_response = requests.get("http://localhost:8000/health", timeout=2)
    #     if health_response.status_code == 200:
    #         api_status.success("✅ API Connected")
    #     else:
    #         api_status.error("❌ API Error")
    # except:
    #     api_status.error("❌ API Offline")

# Main chat interface
st.title("VenkyAI")
st.markdown("Your Personal AI Assistance.")
st.markdown("---")

# Display chat messages
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
                <div class="chat-message user-message">
                    <div class="message-header">
                        👤 You
                    </div>
                    <div class="message-content">
                        {message["content"]}
                    </div>
                    <div class="timestamp">{message.get("timestamp", "")}</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div class="chat-message assistant-message">
                    <div class="message-header">
                    Assistant
                    </div>
                    <div class="message-content">
                        {message["content"]}
                    </div>
                    <div class="timestamp">
                        {message.get("timestamp", "")} 
                        {f"• Response time: {message.get('response_time', 0):.2f}s" if message.get('response_time') else ""}
                    </div>
                </div>
            """, unsafe_allow_html=True)

# Callback to clear input
# def clear_input():
#     st.session_state.user_input = ""

# Chat input
st.markdown("---")

# Before the chat input section, add:
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "clear_input" not in st.session_state:
    st.session_state.clear_input = False

col1, col2 = st.columns([6, 1])

with col1:
    st.text_input(
    "Type your message here...",
    key="widget",  # Changed from "user_input"
    placeholder="Ask me anything...",
    label_visibility="collapsed",
    on_change=submit  # Added this
)
user_input = st.session_state.my_text  # Get value from session state
with col2:
    send_button = st.button("Send 📤", use_container_width=True)
#                                                              ↑ Added this

# Handle message sending
# if send_button and user_input:
#     st.session_state.clear_input = False  # ← Add this first
# After:
if (send_button or st.session_state.enter_pressed) and user_input:
    st.session_state.enter_pressed = False  # Reset flag
    
    # Get current timestamp
    timestamp = datetime.now().strftime("%I:%M %p")
    
    # Add user message to chat history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": timestamp
    })
         
    # Show loading spinner
    with st.spinner(" ✨✨Thinking..."):
        try:

            # Build conversation history
            conversation_history = ""
            for msg in st.session_state.messages[-5:]:  # Last 10 messages
                if msg["role"] == "user":
                    conversation_history += f"User: {msg['content']}\n"
                else:
                    conversation_history += f"Assistant: {msg['content']}\n"

            # Combine history with current query
            query_with_context = f"""Previous conversation:
            {conversation_history}

            Current question: {user_input}

            Please answer the current question while considering the conversation history above."""

            # Call FastAPI endpoint
            response = requests.post(
                API_URL,
                json={"query": query_with_context},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                assistant_message = data["answer"]
                ic(assistant_message)
                response_time = data.get("response_time", 0)
                
                # Add assistant response to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": assistant_message,
                    "timestamp": datetime.now().strftime("%I:%M %p"),
                    "response_time": response_time
                })
            else:
                st.error(f"❌ Error: {response.status_code} - {response.text}")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Sorry, I encountered an error processing your request. Please try again.",
                    "timestamp": datetime.now().strftime("%I:%M %p")
                })
        
        except requests.exceptions.Timeout:
            st.error("⏱️ Request timed out. Please try again.")
            st.session_state.messages.append({
                "role": "assistant",
                "content": "The request took too long. Please try again with a shorter query.",
                "timestamp": datetime.now().strftime("%I:%M %p")
            })
        
        except requests.exceptions.ConnectionError:
            st.error("🔌 Cannot connect to the API. Please make sure the backend is running.")
            st.session_state.messages.append({
                "role": "assistant",
                "content": "I'm having trouble connecting to the server. Please ensure the API is running.",
                "timestamp": datetime.now().strftime("%I:%M %p")
            })
        
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
            st.session_state.messages.append({
                "role": "assistant",
                "content": "An unexpected error occurred. Please try again.",
                "timestamp": datetime.now().strftime("%I:%M %p")
            })

    # st.session_state.clear_input = True


    st.session_state.my_text = ""

 # ← Added this

    
    # Rerun to update the chat display
    st.rerun()

# Welcome message for new users
if len(st.session_state.messages) == 0:
    st.markdown("""
        <div class="chat-message assistant-message">
            <div class="message-header">
                🤖 Assistant
            </div>
            <div class="message-content">
                👋 Hello! I'm your AI assistant. How can I help you today?
                <br><br>
                You can ask me questions about any topic, and I'll do my best to provide helpful and accurate answers.
            </div>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; padding: 1rem;'>"
    "Powered by AI • Made by Venkat"
    "</div>",
    unsafe_allow_html=True
)