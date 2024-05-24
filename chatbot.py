# chatbot.py
# all streamlit components are correctly named. via the most recent version of streamlit
import streamlit as st
import json
import os
from openai import OpenAI


# Load message from file 
# chatbot.py is in the root directory and system_message1.txt is inside the system_messages folder
with open('system_messages/system_message1.txt', 'r') as file:
    message_content = file.read()

# Initialize the OpenAI client
api_key = st.secrets["OPENAI_API_KEY"]
if not api_key:
    st.error("API key not found. Please set the OPENAI_API_KEY environment variable.")
else:
    client = OpenAI(api_key=api_key)



def chatbot_ui():
    st.title("Chat with an AI Dashboard Assistant")
    
    # Initialize session state for messages if not already done
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.api_messages = [
            {"role": "system", "content": message_content}
        ]    

    # Custom CSS to improve chat message visibility and styling
    st.markdown("""
<style>
    /* Targets only the chat input field and not other input elements */
    .stTextInput .st-bk {
        background-color: #ffffff; /* Set desired background color for the input field */
    }

    .stTextInput .st-bk:focus {
        background-color: #ffffff; /* Keeps the background color the same when focused */
    }

    .chat-message {
        padding: 10px;
        margin: 5px;
        border-radius: 20px;
        border: 1px solid #ccc;
    }
    .chat-message.user {
        background-color: #e8f0fe; /* User message background */
        color: black; /* User message text color */
        text-align: right;
        float: right; /* Ensure right alignment */
        clear: both; /* Avoid floating issues */
    }
    .chat-message.assistant {
        background-color: #d1eaff; /* Assistant message background */
        color: black; /* Assistant message text color */
        text-align: left;
        float: left; /* Ensure left alignment */
        clear: both; /* Avoid floating issues */
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
    # Append user message to session states
    current_tab = st.session_state.get('active_tab', 'Unknown')  # Ensure this captures the current state correctly
    user_input_with_context = f"[Current Tab: {current_tab}] {user_input}"

    st.session_state.messages.append({"role": "user", "content": user_input_with_context})
    st.session_state.api_messages.append({"role": "user", "content": user_input_with_context})
    
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
        st.rerun() #experimental_rerun is outdated. rerun is correct. 
