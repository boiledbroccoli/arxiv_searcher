
# ref: https://segmentfault.com/a/1190000044102023
import os, pandas as pd, numpy as np, json
# import plotly.express as px
import streamlit as st
from search_arxiv_summarize import search_summarize
from keyword_generator import keyword_generator
from annotated_text import annotated_text
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder
from summarize_all import summarize_all
from learning_style_calculator import learning_style_calculator


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

language = form.radio(
        "你期望输出的语言是",
        key="language",
        options=["中文", "英文"],
    )
form.markdown('----')
form.markdown('### 学习风格')

questionaire = {}
with open('learning_style_scale.json','r') as f:
    ls_ques = json.load(f)

for key in ls_ques:
    questionaire[key] = form.radio(
        ls_ques[key]['question'],
        ls_ques[key]['choices'],
        index =None
    )
category = learning_style_calculator(questionaire)

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
        rq_submit = st.button("🔼",key = 'rq')
    if research_question == '' and rq_submit:
        st.markdown("❓请输入你的研究问题")
    elif research_question != '' and rq_submit:
        keywords = keyword_generator(research_question, major,language,GPT_API_KEY)
        st.markdown('#### suggested keywords are :')
        cleaned_keywords = keywords.replace("```json", "").replace("```", "").strip()
        kws = json.loads(cleaned_keywords)
        for kw in kws['keywords']:
            # annotated_text((kw['keyword'],"key word"))  # 标记关键词
            annotated_text((kw['keyword']), kw['explanation'])
        

tab1, tab2 = st.tabs(["🔍学术搜索", "👓选出文献"])
columns_show = ['Title','Abstract','Date']

with tab1:
    st.markdown('## ARXIV关键词搜索')
    col1, col2 = st.columns([9, 1])
    with col1:
        keyword = st.text_input("请输入你的关键词:", placeholder="请输入你的关键词:", value="", label_visibility='collapsed')
    with col2:
        kw_submit = st.button("🔍", key='kw')
    
    col3, col4 = st.columns([9,1])
    
    
    with col3:
        focus = st.multiselect(
            "你当前看文献关注的重点是什么",
            ["亮点","理论", "方法", "分析","结论"], placeholder="请选择")
        # print(focus)
        # columns_show += [x for x in focus if x not in columns_show]


    # 检查是否需要初始化或重置 df_data 和 selected_rows
    if 'df_data' not in st.session_state or 'selected_rows' not in st.session_state or 'history_papers' not in st.session_state:
        st.session_state.df_data = pd.DataFrame(columns = columns_show)
        st.session_state.selected_rows = pd.DataFrame(columns = columns_show)
        st.session_state.history_papers = pd.DataFrame(columns = columns_show)

    # 实现更新选中行的函数
    if keyword and kw_submit:
        print(focus)
        st.session_state.df_data = search_summarize(keyword,major,role,language,focus,language,GPT_API_KEY)
    builder = GridOptionsBuilder.from_dataframe(st.session_state.df_data)
    builder.configure_selection('multiple', use_checkbox=True)
    grid_options = builder.build()

    # 使用 AgGrid 显示数据表
    # 显示表格，并通过按钮触发选择读取
    grid_response = AgGrid(
        st.session_state.df_data,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        fit_columns_on_grid_load=True,
        enable_enterprise_modules=True,
        height=300,
        key='dataGrid'
    )

    if st.button("确认选中"):
        selected_rows = pd.DataFrame(grid_response['selected_rows'])
        st.session_state.history_papers = pd.concat([st.session_state.history_papers,selected_rows[columns_show]])
        print(st.session_state.history_papers)
        if not selected_rows.empty:  # 使用.empty来检查DataFrame是否为空
            st.write("选中的标题:")
            for _, selected_row in selected_rows.iterrows():
                st.write(selected_row['Title'])
        else:
            st.write("没有选中的行。")

    # 调试输出当前选中的行数据
        st.write("当前选中的行数据:", selected_rows)

with tab2:
    st.write(st.session_state.history_papers)
    summarise_history = st.button("总结以上文献", key = 'summarise_history')
    if summarise_history:
        summary = summarize_all(st.session_state.history_papers,language,role,major,research_question,keyword,GPT_API_KEY,category = '')
    

    
    