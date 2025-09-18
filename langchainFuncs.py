import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnableBranch, RunnablePassthrough, RunnableLambda
import pandas as pd


# chain = ChatOpenAI(model="gpt-4o", api_key=st.secrets["OPENAIAPIKEY"])

# revenueData = '''
# January   - 3.8  
# February  - 4.2  
# March     - 5.1  
# April     - 4.7  
# May       - 6.3  
# June      - 5.9  
# July      - 6.8  
# August    - 7.4  
# September - 6.6  
# October   - 8.1  
# November  - 9.5  
# December  - 11.2  

# '''

# messages = [
#     SystemMessage(content="You are an ecommerce database agent. [DATA]: " +revenueData),
#     HumanMessage(content="Please tell me the revenue figures for August."),
# ]

# response = chain.invoke(messages)
# print("Full LLM response:", response)
# print("Just the text:", response.content)

def run_chain(user_input):
        #Load data
    df = pd.read_csv('ecommerce_amazon_100.csv')
    print(df.head())

    llm = ChatOpenAI(model="gpt-4o", api_key=st.secrets["OPENAIAPIKEY"])

    #Prompts
    retrieval_prompt = PromptTemplate.from_template(
        '''Based on the following input: '{input_text}', create the appropriate query to be used to filter and return results from a python dataframe (df.query()).
        The dataframe has column values '{col_vals}'. Only return the query to be used inside the df.query function and nothing else'''   
    )
    retrieval_prompt = retrieval_prompt.partial(col_vals = df.columns)

    aggregation_prompt = PromptTemplate.from_template(''' Based on the following : '{input_text}', decide which type of aggregation the user is looking for.
                                                      Choose from 'mean', 'sum', 'count', 'max', 'min' only. Only answer in one of these five values.''')
    
    aggregation_col_prompt = PromptTemplate.from_template(''' Based on the following : '{input_text}' and the following column names '{col_vals}',
                                                           decide which column values is the user looking to aggregate.
                                                       Only answer in one of the dataframe column names provided - no additional info before or after.''')

    aggregation_col_prompt = aggregation_col_prompt.partial(col_vals = df.columns)                                                  

    #Custom functions
    def retrieve_data_func(query_string):
        print("Quesry string Before:", query_string)
        query_string = query_string.replace("```python", "")
        query_string = query_string.replace("```", "")
        query_string = query_string.strip()
        query_string = query_string[1:-1]
        print("Quesry string After:", query_string)

        data = df.query(query_string)
        return data

    def aggregate_func(input):
        print(input)
        retrieved_df = input["retrieved_data"]
        agg_type = input["agg_type"]
        col_name = input["col_name"]

        col_data = retrieved_df[col_name]

        if agg_type == "sum":
            return col_data.mean()
        elif agg_type == "count":
            return col_data.count()

    #Runnable lambda
    retrieve_data = RunnableLambda(retrieve_data_func)
    aggregate = RunnableLambda(aggregate_func)

    #Chain
    retrieval_chain = retrieval_prompt | llm | StrOutputParser() | retrieve_data
    retrieval_chain_passthrough = RunnablePassthrough.assign(retrieved_data = retrieval_chain)

    #Agg type chain
    aggregation_type_chain = aggregation_prompt | llm | StrOutputParser()   
    aggregation_type_passthrough = RunnablePassthrough.assign(agg_type = aggregation_type_chain)


    #Agg col chain
    aggregation_col_chain = aggregation_col_prompt | llm | StrOutputParser()
    aggregation_col_passthrough = RunnablePassthrough.assign(col_name = aggregation_col_chain)

    #Combine to single agg chain
    aggregation_chain = aggregation_type_passthrough | aggregation_col_passthrough | aggregate

    chain = retrieval_chain_passthrough | aggregation_chain


    #Run
    # user_input = {"input_text": "Show me all transactions with the product name Fire TV Stick 4K"}
    
    response = chain.invoke(user_input)
    print(response)
    return response
    
