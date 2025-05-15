import streamlit as st
import requests

st.title("🧠 Mental Health Support Chatbot")
user_id = st.text_input("Enter your username", "guest")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

message = st.text_input("How are you feeling today?")

if st.button("Send"):
    if message:
        response = requests.post("http://localhost:5000/chat", json={"user_id": user_id, "message": message})
        bot_reply = response.json()["response"]
        st.session_state["messages"].append((message, bot_reply))

for user_msg, bot_msg in st.session_state["messages"]:
    st.markdown(f"**You:** {user_msg}")
    st.markdown(f"**Bot:** {bot_msg}")