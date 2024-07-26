
# ref: https://segmentfault.com/a/1190000044102023
import os, pandas as pd, numpy as np
# import plotly.express as px
import streamlit as st
from LLM_search4paper_scholarly import search4paper

#title
st.markdown("# 📕智能学术助手")

form = st.sidebar.form('你的资料')
#defining side bar
form.markdown("**👓你的画像**")

#placing filters in the sidebar using unique values.
role = form.radio(
        "请问你目前是:",
        key="role",
        options=["本科生", "研究生", "研究人员"],
    )

if '生' in role:
    student_year = form.selectbox('请问你目前的年级🧑‍🎓：',key = 'student_year', options = ['一年级','二年级','三年级','四年级','五年级','其他'])
    if '其他' in student_year:
        student_year = form.text_input('请输入你目前的年级：')
else:
    student_year = ''


major = form.text_input(
        "你的专业是："
    )

form.markdown('**❓你的问题**')

rq = form.text_input(
        "你的研究问题："
    )

field = form.text_input(
        "你的研究问题侧重的领域："
    )

form.markdown('**🤖模型选择**')
#placing filters in the sidebar using unique values.
GPT_API_KEY = form.text_input(
        "GPT api KEY:"
    )

model_type = form.radio(
        " 选择你的模型 👉",
        options=[ "gpt-3.5-turbo", "gpt-4", "gpt-4o"],
    )
submitted = form.form_submit_button("提交")


# main page
if submitted:
    
    @st.cache_data
    def get_profile_dataset() -> pd.DataFrame:
        df = search4paper(rq,field,GPT_API_KEY,model_type)
        return df
    # st.dataframe(get_profile_dataset())
    df = get_profile_dataset()
    # st.markdown(df)
    event = st.dataframe(
        df.style.hide(axis="index"),
        # column_config=column_configuration,
        use_container_width=True,
        hide_index=True,
        on_select="rerun",
        selection_mode="multi-row",
    )

    st.markdown("## 选择的文章")
    paper = event.selection.rows
    paper = df.iloc[paper]

    st.dataframe(
        paper.style.hide(axis="index")
        # column_config=column_configuration,
        # use_container_width=True,
    )

    summary4all = st.button('总结以上文章')
    st.markdown("## 选中文章的整体总结")
    if summary4all:
        st.markdown('\n'.join(paper.abstract.tolist()))
else:
    st.markdown('please submit the information on the left')

