import streamlit as st
from openai import OpenAI
from langchainFuncs import run_chain
import pandas as pd


def setupBackend():

    # Create an OpenAI client.
    client = OpenAI(api_key=st.secrets["OPENAIAPIKEY"])

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    # for message in st.session_state.messages:
    #     with st.chat_message(message["role"]):
    #         st.markdown(message["content"])

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if isinstance(message["content"], pd.DataFrame):
                st.dataframe(message["content"])
            else:
                st.write(message["content"])

    return client    

def displayCurrentPrompt(prompt):
    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)    

def llmCall(client):
    # Generate a response using the OpenAI API.
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    ) 
    return stream        

def streamLLMOutput(stream):
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

def chainCall(user_input):
    user_input = {"input_text": user_input}
    return run_chain(user_input)  

def chainCallOutput(chain_response):  
    with st.chat_message("assistant"):
        response = st.write(chain_response)
    st.session_state.messages.append({"role": "assistant", "content": chain_response})    