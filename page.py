
# ref: https://segmentfault.com/a/1190000044102023
import os, pandas as pd, numpy as np, json
# import plotly.express as px
import streamlit as st
from search_arxiv_summarize import search_summarize,translate
from keyword_generator import keyword_generator
from annotated_text import annotated_text
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder
from summarize_all import summarize_all
from learning_style_calculator import learning_style_calculator



# title

st.set_page_config(page_title="智能学术助手", page_icon="📕", layout="wide")




# left side-bar -- navigation
# 调整 sidebar 宽度
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
st.sidebar.markdown('## 🧭页面导航')

if st.sidebar.button("STEP1: 个人资料🧑‍🎓"):
    st.session_state.current_page = 'page_info'
if st.sidebar.button("STEP2: 关键词建议🧑‍🎓"):
    st.session_state.current_page = 'page_keyword'
if st.sidebar.button("STEP3: 学术搜索🔍"):
    st.session_state.current_page = 'page_search'
if st.sidebar.button("STEP4: 选择文献✅"):
    st.session_state.current_page = 'page_selected'



def page_info(): # 包含实用指南和个人信息收集

    if 'major' not in st.session_state:
        st.session_state.major = ''
    if 'role1' not in st.session_state:
        st.session_state.role1 = '本科生'
    if 'language1' not in st.session_state:
        st.session_state.language1 = '中文'
    if 'category' not in st.session_state:
        st.session_state.category = ''
    # if 'GPT_API_KEY' not in st.session_state:
    #     st.session_state.GPT_API_KEY = st.secrets['api_key']

    st.markdown("# 📕智能学术助手")
    with st.expander("**💡 使用指南**", expanded=True):
    
        steps = """
        **Step 1:** 在左侧的 <span style="color:#2E86C1;"><b>个人资料模块</b></span> 填入您的专业、年级、输出语言和学习风格等信息。
    
        **Step 2:** 在 <span style="color:#16A085;"><b>关键词搜索建议模块</b></span> 中，输入研究问题，获取关键词和搜索建议。
    
        **Step 3:** 在 <span style="color:#D35400;"><b>学术搜索模块</b></span> 中输入关键词，搜索相关文献；可选择关注重点内容，生成个性化总结。
    
        **Step 4:** 在输出的文献中可以 <span style="color:#1ABC9C;"><b>选中感兴趣的文献加入文献库</b></span>，并生成一个汇总总结。
    
        **Step 5:** 在 <span style="color:#8E44AD;"><b>选出文献模块</b></span> 中查看历史文献库，并可生成汇总总结。

        🔼 所有结果运行完成之前请不要变换页面，这会让进行中的程序中断🔼
        
        """
        
        st.markdown(steps, unsafe_allow_html=True)

    
    st.markdown('## 🧑‍🎓个人资料')

    form = st.form('个人资料')
    st.session_state.major = form.text_input(
            "你的专业是：",value  = st.session_state.major
        )


    #placing filters in the sidebar using unique values.
    st.session_state.role1 = form.radio(
            "请问你目前是:",
            key="role",
            options=["本科生", "研究生", "研究人员"],
            index = ["本科生", "研究生", "研究人员"].index(st.session_state.role1)
            
        )

    st.session_state.language1 = form.radio(
            "你期望输出的语言是",
            key="language",
            options=["中文", "英文"],
            index = ["中文", "英文"].index(st.session_state.language1)
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
    st.session_state.category = learning_style_calculator(questionaire)

    form.markdown('----')

    submitted = form.form_submit_button("提交")
    
    if submitted:
        if st.session_state.major == ""  or \
        st.session_state.language1 == "" or not questionaire : # 改
            st.sidebar.error("请填写所有必填信息。")
        else:
            # 显示成功提示
            st.sidebar.success("完成！请进入STEP2输入研究问题，开启学术阅读之旅🎈")
            st.balloons()




if 'current_page' not in st.session_state:
    st.session_state.current_page = 'page_info'

# main page
def page_keyword():
    major = st.session_state.major
    role = st.session_state.role1
    language = st.session_state.language1
    category = st.session_state.category
    GPT_API_KEY = st.secrets['api_key']
    st.markdown("# 📕智能学术助手")
    if 'keyword_results' not in st.session_state:
        st.session_state.keyword_results = None  # For storing keyword suggestions results

    if 'df_data' not in st.session_state or 'history_papers' not in st.session_state:
        st.session_state.df_data = pd.DataFrame(columns = [ 'Title', 'Date','Abstract'])  # For storing search results in Tab 1
        st.session_state.history_papers = pd.DataFrame(columns = ['Title', 'Date','Abstract'])

    # with st.expander("**💡关键词搜索建议**"):
    col1, col2 = st.columns([9,1]) 
    with col1:
        research_question = st.text_input("你的研究问题：",placeholder="请输入你的研究问题", value="",label_visibility='collapsed')
    with col2:
        rq_submit = st.button("🔍",key = 'rq')
    if research_question == '' and rq_submit:
        st.markdown("❓请输入你的研究问题")
    elif research_question != '' and rq_submit:
        keywords = keyword_generator(research_question,language,GPT_API_KEY)
        st.markdown('## 关键词建议:')
        cleaned_keywords = keywords.replace("```json", "").replace("```", "").strip()
        print(cleaned_keywords)
        kws = json.loads(cleaned_keywords)
        st.session_state.keyword_results = kws  # Store in session state
    if st.session_state.keyword_results:
        for kw in st.session_state.keyword_results['keywords']:
            # annotated_text((kw['keyword'],"key word"))  # 标记关键词
            annotated_text((kw['keyword'], ""))  # Display keyword in boxed format
            # Add explanation in smaller font on a new line using st.markdown
            st.markdown(f"<p style='font-size: 14px;'>{kw['explanation']}</p>", unsafe_allow_html=True)
    st.session_state.research_question = research_question
          

# tab1, tab2 = st.tabs(["🔍学术搜索", "👓选出文献"])


def page_search():
    major = st.session_state.major
    role = st.session_state.role1
    language = st.session_state.language1
    category = st.session_state.category
    GPT_API_KEY = st.secrets['api_key']
    research_question = st.session_state.research_question

    if 'focus' not in st.session_state:
        st.session_state.focus = []
    st.markdown("# 📕智能学术助手")
    st.markdown('## ARXIV关键词搜索')
    keyword = st.text_input("请输入你的关键词:", placeholder="请输入")

    # Multi-select for focus areas
    st.session_state.focus = st.multiselect(
        "你当前看文献关注的重点是什么",
        ["亮点", "理论", "方法", "分析", "结论"], 
        placeholder="请选择",
        default = st.session_state.focus
    )
    focus = st.session_state.focus
    kw_submit = st.button("提交进行搜索 🔍", key='kw')

    if keyword and kw_submit:
        st.session_state.df_data = search_summarize(keyword,major,role,language,focus,category,GPT_API_KEY)
        st.info("【使用小贴士】可以通过**选中后拖动**来改变列的顺序")

    builder = GridOptionsBuilder.from_dataframe(st.session_state.df_data)
    builder.configure_selection('multiple', use_checkbox=True)


    builder.configure_column(
    'Abstract',
    wrapText=True,        # Enable text wrapping inside the cells
    autoHeight=True,      # Allow row height to adjust based on content
    width=800             # Set specific width for the 'abstract' column
    )

    builder.configure_column(
        'Title',
        wrapText=True,        
        autoHeight=True,      
        width=400             # Set specific width for the 'title' column
    )

    builder.configure_column(
        'Date',
        wrapText=True,        
        autoHeight=True,      
        width=100             # Set specific width for the 'date' column
    )

    for col in st.session_state.df_data.columns:
        if col not in ['Abstract', 'Title', 'Date']:
            builder.configure_column(
                col,
                wrapText=True,    # Enable text wrapping for other columns
                autoHeight=True,  # Allow auto height adjustment based on content
                width=400         # Set a general width of 400 for unspecified columns
            )


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
        # domLayout='autoHeight',
        key='dataGrid'
    )
    # print(f"!!!!!!!!!!!!!!1\n{st.session_state.df_data}")

    if st.button("确认选中并总结"):
        selected_rows = pd.DataFrame(grid_response['selected_rows'])
        st.session_state.history_papers = pd.concat([st.session_state.history_papers,grid_response['selected_rows']])
        if not selected_rows.empty:  # 使用.empty来检查DataFrame是否为空
            st.write("选中的标题:")
            for _, selected_row in selected_rows.iterrows():
                st.write(selected_row['Title'])
            summary_selected = summarize_all(selected_rows,language,role,major,research_question,focus,GPT_API_KEY,category)
        else:
            st.write("没有选中的行。")
        
        print(summary_selected)

    # 调试输出当前选中的行数据
        st.write("当前选中的行数据:", selected_rows)
        container_t1 = st.container(border=True)
        container_t1.write("### 选中文献总结")
        container_t1.write(summary_selected)


def page_selected():
    major = st.session_state.major
    role = st.session_state.role1
    language = st.session_state.language1
    category = st.session_state.category
    GPT_API_KEY = st.secrets['api_key']
    research_question = st.session_state.research_question
    focus = st.session_state.focus
    
    history_papers = AgGrid(
        st.session_state.history_papers,
        update_mode=GridUpdateMode.MODEL_CHANGED
    )
    summary = ''
    summarise_history = st.button("总结以上文献", key = 'summarise_history')
    if summarise_history:
        summary = summarize_all(st.session_state.history_papers,language,role,major,research_question,focus,GPT_API_KEY,category)
    container = st.container(border=True)
    container.write("## 文献总结")
    container.write(summary)

    



if st.session_state.current_page == 'page_info':
    page_info()
elif st.session_state.current_page == 'page_keyword':
    page_keyword()
elif st.session_state.current_page == 'page_search':
    page_search()
elif st.session_state.current_page == 'page_selected':
    page_selected()
