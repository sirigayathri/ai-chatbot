import streamlit as st
from google import genai

# Load API key securely
client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

st.title("🤖 AI Chatbot")

# -------------------------------
# Chat memory
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
st.sidebar.title("Menu")
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()

# -------------------------------
# Show messages
# -------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------------
# Input
# -------------------------------
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.models.generate_content(
                    model="models/gemini-1.5-flash",
                    contents=user_input
                )
                reply = response.text
            except:
                reply = "⚠️ API limit reached or unavailable."

            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
