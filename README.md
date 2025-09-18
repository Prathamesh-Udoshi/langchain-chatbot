# LangChain Chatbot for E-commerce CSV Analysis

A Streamlit-based chatbot that lets you query your e-commerce data via natural language. Powered by LangChain + OpenAI, it ingests CSV data into a DataFrame and allows you to ask questions, perform aggregate operations, filters, and more.

---

## Features

- **Natural Language Queries**: Type human-friendly questions (e.g. “What was our total revenue last quarter for electronics?”).  
- **DataFrame Access**: Reads e-commerce CSV data and loads into pandas DataFrame.  
- **Filtering & Aggregation**: Supports standard operations like sum, count, average, group by, min/max.  
- **Responsive UI**: Streamlit frontend for easy interaction.  
- **OpenAI / LangChain Backend**: Uses LangChain to parse user intent and generate DataFrame operations under the hood.  
- **Error Handling**: Gracefully handles mis-phrased queries or ambiguous requests (assuming implemented).  

---

## How It Works (Architecture)

1. **Load Data**  
   At start, the application loads an e-commerce CSV file.  

2. **User Input**  
   Through Streamlit UI, user inputs a natural language question / query.  

3. **LangChain Processing**  
   The query is processed via a prompt in LangChain, possibly with examples/templates, to map the question to DataFrame code (filters, aggregations, etc.).

4. **Execution**  
   The code generated is executed on the DataFrame (pandas), computing the result.

5. **Output**  
   The result is presented in the UI: could be a table, a number/statistic, or textual summary.

---

## Installation / Setup

1. Clone the repository:  
   ```bash
   git clone https://github.com/Prathamesh-Udoshi/langchain-chatbot.git
   cd langchain-chatbot


### How to run it on your own machine

1. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

2. Run the app

   ```
   $ streamlit run streamlit_app.py
   ```
