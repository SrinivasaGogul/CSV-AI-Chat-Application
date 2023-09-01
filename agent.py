import pandas as pd
from langchain.llms import OpenAI
from langchain.agents import create_csv_agent, create_pandas_dataframe_agent
import os
import dotenv


dotenv.load_dotenv('key.env', override=True)
API_KEY = os.getenv('OPENAI_API_KEY')


def create_agent(filename) -> str:
    
    llm = OpenAI(openai_api_key = API_KEY)


    df = pd.read_csv(filename)

    return create_pandas_dataframe_agent(llm, df, verbose=True)

def query_agent(agent, query):

    prompt = (
        """
            For the following query, if it requires drawing a table, reply as follows:
            {"table": {"Name of the column": ["Data 1", "Data 2", ...], "Name of the Column": ["Data 1", "Data 2", ...], "Name of the Column": ["Data 1", "Data 2", ...], ...]}}

            for example {"table": {"Countries": ["India", "Singapore", "United States of America"], "Population": [12345, 23456, 12112], ...}}
            use the above format only for table if the query requires to draw a table.

            If the query requires creating a bar chart, reply as follows:
            {"bar": {"x_axis": ["A", "B", "C", ...], "y_axis": [25, 24, 10, ...], "column_name": ["name of the data passed in x_axis", "name of the data passed in y_axis"]}}
            
            If the query requires creating a line chart, reply as follows:
            {"line": {"x_axis": ["A", "B", "C", ...], "y_axis": [25, 24, 10, ...], "column_name": ["name of the data passed in x_axis", "name of the data passed in y_axis"]}}
            
            There can only be two types of chart, "bar" and "line".

            for each reply "column_name" is must give appropriate names as per the data passed in x_axis and y_axis 

            dont use single quotes('') anywhere in the reply insted use double quotes("") and return a JSON String
            
            If it is just asking a question that requires neither, reply as follows:
            {"answer": "answer"}
            
            Example:
            {"answer": "The title with the highest rating is 'Gilead'"}
            
            If you do not know the answer, reply as follows:
            {"answer": "I do not know."}
            
            Return all output as a string.
            
            All strings in "columns" list and data list, should be in double quotes,
            
            For example: {"x_axis":["america", "india",...], "y_axis": [223, 456, ...], "column_name": ["countries", "rating"]}

            dont use single quotes('') anywhere in the reply insted use double quotes("") and return a JSON String
            
            Lets think step by step.
            
            give the answer in above given format only.
            
            Below is the query.
            Query: 
            """
        + query
    )
    response = agent.run(prompt)

    return response.__str__()
    

