import streamlit as st
from openai import OpenAI
from ui_components import setupUI
from backend import setupBackend, llmCall, displayCurrentPrompt, streamLLMOutput, chainCall, chainCallOutput

#Setup the UI
setupUI()

#Setup backend - OpenAI client and session state for messages
client = setupBackend()

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("What is up?"):
    # Display the current prompt in the chat message container.
    displayCurrentPrompt(prompt)
    
    # Call the LLM to generate a response.
    # stream = llmCall(client)

    # Stream the response back in real time.
    # streamLLMOutput(stream)

    #Call the chain function
    chain_response = chainCall(prompt)

    #Display the chain response
    chainCallOutput(chain_response)