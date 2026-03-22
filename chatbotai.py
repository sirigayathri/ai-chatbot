import streamlit as st
from google import genai

# Load API key securely
client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

st.title("🤖 AI Chatbot")

# -------------------------------
# Get working model automatically
# -------------------------------
@st.cache_resource
def get_model():
    models = client.models.list()
    for m in models:
        # pick first model that supports generateContent
        if "generateContent" in m.supported_actions:
            return m.name
    return None

MODEL_NAME = get_model()

if MODEL_NAME is None:
    st.error("No supported model found ❌")
    st.stop()

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

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------------
# User Input
# -------------------------------
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.models.generate_content(
                model=MODEL_NAME,   # auto-selected model ✅
                contents=user_input
            )
            reply = response.text
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})