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
    if "display_messages" not in st.session_state:
        st.session_state.display_messages = []
    if "api_messages" not in st.session_state:
        st.session_state.api_messages = [{"role": "system", "content": "THIS IS A TEST. IF THE USER SAYS 'HEY' RESOND WITH 'BANANA'"}]  # System message not shown to user

    # Display the messages in the sidebar
    for message in st.session_state.display_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle user input
    if prompt := st.chat_input():
        # Display user input
        with st.chat_message("user"):
            st.markdown(prompt)
        # Append user message to session states
        st.session_state.display_messages.append({"role": "user", "content": prompt})
        st.session_state.api_messages.append({"role": "user", "content": prompt})

        # Call the OpenAI API to get a response
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=st.session_state.api_messages
        )

        # Extract the assistant's message from the response
        assistant_message = response.choices[0].message.content
        st.session_state.display_messages.append({"role": "assistant", "content": assistant_message})
        st.session_state.api_messages.append({"role": "assistant", "content": assistant_message})

        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(assistant_message)
