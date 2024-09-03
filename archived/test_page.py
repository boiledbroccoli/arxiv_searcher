import os, pandas as pd, numpy as np, json
# import plotly.express as px
import streamlit as st
st.markdown(
    f'''
        <style>
            .sidebar .sidebar-content {{
                width: 375px;
            }}
        </style>
    ''',
    unsafe_allow_html=True
)
st.sidebar.write("button")
if st.sidebar.button('页面1'):
    st.session_state.current_page = 'page1'
if st.sidebar.button('页面2'):
    st.session_state.current_page = 'page2'

def page1():
    st.title('页面1')
    st.write('这是页面1的内容。')
    number = st.text_input("Enter some value here ")
    
    
    if st.button('切换到页面2'):
        st.session_state.current_page = 'page2'
        if st.session_state.status == 0:
            st.session_state.number = int(number)
        else:
            st.session_state.number += int(number)
        st.session_state.status +=1


def page2():
    st.title('页面2')
    st.write('这是页面2的内容。')
    st.write(f'number sum in page 1 : {st.session_state.number}')
    if st.button('切换到页面1'):
        st.session_state.current_page = 'page1'

if 'current_page' not in st.session_state:
    st.session_state.current_page = 'page1'
    st.session_state.number = '-'
    st.session_state.status = 0
if st.session_state.current_page == 'page1':
    page1()
else:
    page2()