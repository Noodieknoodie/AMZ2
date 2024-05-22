# chatbot.py
import streamlit as st
import openai
import os
openai.api_key = os.getenv('OPENAI_API_KEY')
def get_chatgpt_response(messages):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=messages
        )
        return response.choices[0].message['content']
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return "Sorry, I encountered an error. Please try again later."
def render_chatbot(chat_history):
    st.header("Chatbot")
    for message in chat_history:
        if message['role'] == 'user':
            st.write(f"<p style='color:blue;'><b>You:</b> {message['content']}</p>", unsafe_allow_html=True)
        else:
            st.write(f"<p><b>Assistant:</b> {message['content']}</p>", unsafe_allow_html=True)
    user_input = st.text_area("You:", "", key="user_input", height=150)
    if st.button("Send"):
        if user_input:
            chat_history.append({"role": "user", "content": user_input})
            with st.spinner("Generating response..."):
                response = get_chatgpt_response(chat_history)
            chat_history.append({"role": "assistant", "content": response})
            st.rerun()
    if st.button("Clear Conversation"):
        chat_history = [chat_history[0]]
        st.rerun()
