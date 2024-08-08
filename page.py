
# ref: https://segmentfault.com/a/1190000044102023
import os, pandas as pd, numpy as np
# import plotly.express as px
import streamlit as st
from search_arxiv_summarize import search_summarize
from keyword_generator import keyword_generator
from annotated_text import annotated_text
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
from summarize_all import summarize_all



# document-loading
## tutorial
with open('mainpage-tutorial.txt','r') as f:
    tutorial_content = f.read()



# title
st.set_page_config(page_title="智能学术助手", page_icon="📕", layout="wide")
st.markdown("# 📕智能学术助手")


# left side-bar
st.sidebar.markdown('## 🧑‍🎓个人资料')

form = st.sidebar.form('个人资料')
major = form.text_input(
        "你的专业是："
    )

#placing filters in the sidebar using unique values.
role = form.radio(
        "请问你目前是:",
        key="role",
        options=["本科生", "研究生", "研究人员"],
    )


form.markdown('----')
form.markdown('**🤖CHATGPT**')
#placing filters in the sidebar using unique values.
GPT_API_KEY = form.text_input(
        "GPT api KEY:"
    )

# model_type = form.radio(
#         " 选择你的模型 👉",
#         options=[ "gpt-3.5-turbo", "gpt-4", "gpt-4o"],
#     )
submitted = form.form_submit_button("提交")




# main page

with st.expander("**💡使用指南**"):
    st.write(tutorial_content)

with st.expander("**💡关键词搜索建议**",expanded =True):
    col1, col2 = st.columns([9,1]) 
    with col1:
        research_question = st.text_input("你的研究问题：",placeholder="请输入你的研究问题", value="",label_visibility='collapsed')
    with col2:
        rq_submit = st.button("🔍",key = 'rq')
    if research_question == '' and rq_submit:
        st.markdown("❓请输入你的研究问题")
    elif research_question != '' and rq_submit:
        keywords = keyword_generator(research_question, GPT_API_KEY)
        st.markdown('#### suggested keywords are :')
        for kw in keywords:
            annotated_text((kw,"key word"),f":\n {keywords[kw]}")
        

tab1, tab2 = st.tabs(["🔍学术搜索", "👓选出文献"])

with tab1:
    st.markdown('## ARXIV关键词搜索')
    col1, col2 = st.columns([9,1]) 
    with col1:
        keyword = st.text_input("请输入你的关键词:",placeholder="请输入你的关键词:", value="",label_visibility='collapsed')    
    with col2:
        kw_submit = st.button("🔍",key = 'kw')
    
    col3, col4 = st.columns([1,1])
    history_papers = pd.DataFrame()
    with col3:
        focus= st.selectbox("你的关注重点: ",("亮点","理论", "方法", "分析","结论"),) # 关注重点 ：需要改
        expected_language = st.text_input("总结时期望的语言？",placeholder="中文")
    if keyword != "" and kw_submit:
        search_results = search_summarize(keyword,focus,expected_language,GPT_API_KEY,)
        
        search_papers = AgGrid(search_results, 
                               use_checkbox = True) # 搜索的文献结果 ：需要改
        chosen_papers = search_papers['selected_row'] # 选择文献的结果 ：需要改
        history_papers = pd.concat([history_papers,chosen_papers],axis = 1)
        with tab2:
            AgGrid(history_papers)
            st.button('summarize')
            st.dataframe(chosen_papers) 
        ifsummarize = st.button("summarize")
        if ifsummarize:
            summary_total = summarize_all(chosen_papers)
            st.markdown(f'### 选中文献总结: \n { summary_total}')
    elif keyword =="" and kw_submit:
        st.markdown("🙋请输入关键词")

'''
有一些问题：
* ifsummarize点击后没有文献框全部消失（应该跟多个 button 之间的关系有关）
* chosen papers 是否能在 tab2中存在
focus 那里需要变成多选的
所有的口都没写
'''
    
    