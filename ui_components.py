import streamlit as st
from openai import OpenAI

def setupUI():
    #Sidebar with dropdown to select data source
    selected_data_source = st.sidebar.selectbox(
    "Select your dataset:",
    ("Table A", "Table B")
    )

    #Write out the selection
    st.write(f"You selected: {selected_data_source}")

    # Show title and description.
    st.title("💬 Ecommerce Analytics Chatbot")
    st.write(
    "This is a simple chatbot that uses OpenAI's GPT-4o-mini model to generate responses. "
    "This bot lets you analyze data and create visualizations using natural language." 
    )
