import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Streamlit UI setup
st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")
st.title("🤖ChatBot")

# Keep chat history in session (persists until refresh)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history with chat bubbles
for role, text in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(text)

# Input box at the bottom
if prompt := st.chat_input("Type your message..."):
    # Add user message
    st.session_state.messages.append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # Build conversation history for Gemini
    history = []
    for role, text in st.session_state.messages:
        if role == "user":
            history.append({"role": "user", "parts": [text]})
        else:
            history.append({"role": "model", "parts": [text]})

    # Call Gemini with full history
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(history)
        bot_reply = response.text
    except Exception as e:
        bot_reply = f"Error: {e}"

    # Add bot reply
    st.session_state.messages.append(("assistant", bot_reply))
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
