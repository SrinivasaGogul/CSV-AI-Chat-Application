import streamlit as st
import pandas as pd
import json
from agent import create_agent, query_agent
from mimetypes import guess_type
import mimetype
import altair as alt
import plotly.express as px
def response_typecast(response:str):

    return json.loads(response)

st.title('👨‍💻 Chat with your CSV')

st.write('Please upload your CSV file below')

data = st.file_uploader('Upload a CSV')

if "messages" not in st.session_state:
    st.session_state.messages = []
 
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        if message['role'] == 'user':
            st.markdown(message['content'])

        else:
            if 'bar' in message['content']:
                column_name = message['content']['bar'].pop('column_name')
                his_data = {column_name[0]: message['content']['bar']['x_axis'], column_name[-1]: message['content']['bar']['y_axis']}
                df = pd.DataFrame(his_data)
                message['content']['bar'].update({'column_name':column_name})
                chart = px.bar(df, x = column_name[0], y = column_name[-1])
                st.write(chart)
                # chart = alt.Chart(df).mark_bar().encode(x =column_name[0], y = column_name[-1])
                # chart.properties(width = 600, height = 400)
                # st.altair_chart(chart, use_container_width=True)

            elif 'line' in message['content']:
                column_name = message['content']['line'].pop('column_name')
                his_data = {column_name[0]: message['content']['line']['x_axis'], column_name[-1]: message['content']['line']['y_axis']}
                df = pd.DataFrame(his_data)
                message['content']['line'].update({'column_name':column_name})
                chart = alt.Chart(df).mark_line().encode(x =column_name[0], y = column_name[-1])
                chart.properties(width = 600, height = 400)
                st.altair_chart(chart, use_container_width=True)

            elif 'table' in message['content']:
                msg_data = message['content']['table']
                df = pd.DataFrame(msg_data)
                st.table(df)
            
            else:
                msg_data = message['content']
                st.markdown(msg_data)
        

def write_response(response_dict):

    with st.chat_message('assistant'):

        if 'answer' in response_dict:
            st.markdown(response_dict['answer'])
            st.session_state.messages.append({"role": 'assistant', 'content': response_dict['answer']})

        if 'bar' in response_dict:
            column_name = response_dict['bar'].pop('column_name')
            msg_data = {column_name[0]: response_dict['bar']['x_axis'], column_name[-1]: response_dict['bar']['y_axis']}
            df = pd.DataFrame(msg_data)
            response_dict['bar'].update({"column_name":column_name})
            message['content']['bar'].update({'column_name':column_name})
            chart = px.bar(df, x = column_name[0], y = column_name[-1])
            st.write(chart)
            # chart = alt.Chart(df).mark_bar().encode(x =column_name[0], y = column_name[-1])
            # chart.properties(width = 600, height = 400)
            # st.altair_chart(chart, use_container_width=True)   
            st.session_state.messages.append({"role": 'assistant', "content":{'bar':response_dict['bar']}})
        
        if "line" in response_dict:
            column_name = response_dict['line'].pop('column_name')
            msg_data = {column_name[0]: response_dict['line']['x_axis'], column_name[-1]: response_dict['line']['y_axis']}
            df = pd.DataFrame(msg_data)
            response_dict['line'].update({"column_name":column_name})
            chart = alt.Chart(df).mark_line().encode(x = column_name[0], y = column_name[-1])
            chart.properties(width= 600, height = 400)
            st.altair_chart(chart, use_container_width=True)
            st.session_state.messages.append({'role': 'assistant', 'content':{'line':response_dict['line']}})

        if "table" in response_dict:
            msg_data = response_dict['table']
            df = pd.DataFrame(msg_data)
            st.table(df)
            st.session_state.messages.append({'role':'assistant', 'content': {'table':response_dict['table']}})

prompt = st.chat_input('Ask some questions about your CSV')

# if st.button('Submit', type="primary"):
if data and prompt:

    if "messages" not in st.session_state:
        st.session_state.messages = []
    with st.chat_message('user'):
        st.markdown(prompt)
        st.session_state.messages.append({'role': 'user', 'content': prompt})

    agent = create_agent(data)

    response = query_agent(agent=agent, query=prompt)

    decode = response_typecast(response)

    write_response(decode)

