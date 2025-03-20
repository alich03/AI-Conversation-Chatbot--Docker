import streamlit as st
import requests
import time

# API Endpoints http://rag-api:5000
BASE_URL = "http://rag-api:8000"
UPLOAD_API_URL = f"{BASE_URL}/api/upload"
CHAT_API_URL = f"{BASE_URL}/api/chat"

# App configuration
st.set_page_config(page_title="AI Chatbot", layout="wide")

# Sidebar for PDF upload
st.sidebar.header("Upload PDF")
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file:
    st.sidebar.info("Uploading PDF...")

    try:
        # Send file to API
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        response = requests.post(UPLOAD_API_URL, files=files)
        response_json = response.json()

        if response.status_code == 200:
            document_id = response_json.get("document_id", "N/A")
            st.sidebar.success(f"✅ PDF uploaded successfully! Document ID: {document_id}")
        else:
            st.sidebar.error(f"❌ Upload failed: {response_json.get('message', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        st.sidebar.error(f"⚠️ API Error: {str(e)}")

# Main chat interface
st.title("📄 AI Conversational Chatbot")
st.write("Upload a PDF and start chatting!")

# Initialize chat history
if "history" not in st.session_state:
    st.session_state["history"] = []

# Display previous messages
for question, response in st.session_state["history"]:
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        st.markdown(response)

# Chat input
user_input = st.chat_input("Type your message here...")

# Handle chat input
if user_input:
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    if "history" not in st.session_state:
        chat_history = [("who are you","i am AI CONVERSATION CHATBOT created by ALI HASNAIN.")]
    else:
        chat_history = st.session_state["history"]



    # API request payload
    payload = {"message": user_input,"chat_history":chat_history}

    try:
        # Send request to chatbot API
        chat_response = requests.post(CHAT_API_URL, json=payload)
        chat_response_json = chat_response.json()

        if chat_response.status_code == 200:
            bot_message = chat_response_json.get("message", "No response received.")

            # Append to chat history
            st.session_state["history"].append((user_input, bot_message))

     
            with st.chat_message('assistant'):
                progress_text = st.empty()

                for i in range(len(bot_message)):
                    progress_text.markdown(bot_message[:i + 1])
                    time.sleep(0.0005)

        else:
            error_message = chat_response_json.get("message", "Unknown error.")
            st.session_state["history"].append((user_input, f"❌ Error: {error_message}"))
            with st.chat_message("assistant"):
                st.error(f"❌ Error: {error_message}")

    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ API Error: {str(e)}")
