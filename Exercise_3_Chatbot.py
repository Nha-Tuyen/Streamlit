import streamlit as st
from hugchat import hugchat
from hugchat.login import Login

# Create App title
st.title("Simple Chatbot")

# Hugging Face Credentials
with st.sidebar:
    st.title("Login Hugchat")
    hf_email = st.text_input("Enter Email: ")
    hf_password = st.text_input("Enter Password: ", type="password")
    if not (hf_email and hf_password):
        st.warning("Please enter your account!", icon='⚠')
    else:
        st.success("Proceed to entering your prompt message!", icon='👉')

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How may I help you?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


# Function for generating LLM response
def generate_response(prompt_input, email, passwd):
    # Hugging Face Login
    sign = Login(email, passwd)
    cookies = sign.login()
    # Create ChatBot
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    return chatbot.chat(prompt_input)


# User-provided prompt
if prompt := st.chat_input(disabled=not (hf_email and hf_password)):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Check if the last message is not from the assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Assistant is typing..."):
            response = generate_response(prompt, hf_email, hf_password)
            st.write(response)
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)
