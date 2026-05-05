import streamlit as st
import requests

API_KEY = st.secrets["OPENROUTER_API_KEY"]

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 AI Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "openai/gpt-3.5-turbo",
                    "messages": st.session_state.messages
                }
            )

            data = response.json()

            if "choices" in data:
                reply = data["choices"][0]["message"]["content"]
            else:
                reply = f"⚠️ API Error: {data}"

        except Exception as e:
            reply = f"⚠️ Error: {str(e)}"

        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
