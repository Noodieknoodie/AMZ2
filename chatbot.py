import streamlit as st
import json
import os
from openai import OpenAI

# Load system message
with open('system_messages/system_message1.txt', 'r') as file:
    message_content = file.read()

# Initialize the OpenAI client
try:
    api_key = st.secrets.get("OPENAI_API_KEY", None)
    if api_key:
        client = OpenAI(api_key=api_key)
    else:
        client = None
except Exception:
    client = None



def chatbot_ui():
    st.title("Chat with an AI Dashboard Assistant")
    
    if client is None:
        st.warning("AI Chat is unavailable. Please configure OpenAI API key in Streamlit Cloud secrets.")
        return
    
    # Initialize session state for messages if not already done
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.api_messages = [
            {"role": "system", "content": message_content}
        ]    

    # Custom CSS for chat messages
    st.markdown("""
<style>
    .chat-message {
        padding: 10px;
        margin: 5px;
        border-radius: 20px;
        border: 1px solid #ccc;
    }
    .chat-message.user {
        background-color: #e8f0fe;
        color: black;
        text-align: right;
        float: right;
        clear: both;
    }
    .chat-message.assistant {
        background-color: #d1eaff;
        color: black;
        text-align: left;
        float: left;
        clear: both;
    }
</style>
    """, unsafe_allow_html=True)

    # Display the messages
    for message in st.session_state.messages:
        with st.container():
            role_class = "user" if message["role"] == "user" else "assistant"
            st.markdown(f'<div class="chat-message {role_class}">{message["content"]}</div>', unsafe_allow_html=True)

    # Handle user input
    user_input = st.chat_input("Type your message...", key="user_input")
    if user_input is not None:
        process_user_input(user_input)

def process_user_input(user_input):
    if client is None:
        return
        
    # Append user message to session states
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.api_messages.append({"role": "user", "content": user_input})
    
    try:
        # Call the OpenAI API to get a response
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=st.session_state.api_messages
        )
        # Extract the assistant's message from the response
        assistant_message = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})
        st.session_state.api_messages.append({"role": "assistant", "content": assistant_message})
        
        # Immediate display update after API call
        st.rerun()
    except Exception as e:
        st.session_state.messages.append({"role": "assistant", "content": f"Failed to get response: {e}"})
        st.rerun() 