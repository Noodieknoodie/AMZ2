import streamlit as st
import os
from openai import OpenAI

# Initialize the OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("API key not found. Please set the OPENAI_API_KEY environment variable.")
else:
    client = OpenAI(api_key=api_key)

def chatbot_ui():
    st.title("Chat with GPT-4 Turbo")
    
    # Initialize session state for messages if not already done
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.api_messages = [
            {"role": "system", "content": "This is a test. If the user says 'hey', say 'BANANA'."}
        ]

    # Display the messages using Streamlit's chat_message
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Handle user input
    user_input = st.chat_input("Type your message...", key="user_input")
    if user_input is not None:
        process_user_input(user_input)

def process_user_input(user_input):
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

# this is a module fyi not a standalone
