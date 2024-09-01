
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

if submitted:
    st.balloons()
    if not major or not role or not language or not questionaire:
        st.sidebar.error("请填写所有必填信息。")
    else:
        # 显示成功提示
        st.sidebar.success("完成！快输入研究问题，开启学术阅读之旅🎈")



# main page
  

with st.expander("**💡使用指南**",expanded =True):
    # st.write(tutorial_content)
    # st.write(f"# {label}")    

    # 定义不同的样式
    style = """
    <style>
        .title {
            font-size: 20px;
            color: #2E86C1; 
            font-weight: bold;
        }
        .subtitle {
            font-size: 18px;
            color: #16A085; 
            font-weight: bold;
        }
        .step {
            font-size: 16px;
            color: #E74C3C; 
            font-weight: bold;
        }
        .text {
            font-size: 14px;
            color: #34495E; 
        }
        ul.text {
        padding-left: 14px;
        margin: 5px 5px;
        }
        ul.text li {
            font-size: 14px;
            color: #34495E; 
            line-height: 1;
        }
    </style>
    """

    # 插入样式到 Streamlit
    st.markdown(style, unsafe_allow_html=True)

    # 显示不同层级的文本
    st.markdown("<p class='title'>欢迎来到您的研究小助手！</p>", unsafe_allow_html=True)
    st.markdown("<p class='text'>不管您是学术小白还是科研大佬，这里都能让您的研究过程更轻松！跟着这几个步骤，让我们开始吧！</p>", unsafe_allow_html=True)

    st.markdown("<p class='step'>Step 1: 先完善个人信息</p>", unsafe_allow_html=True)
    st.markdown("<p class='text'>在左侧的个人资料模块填入这些信息：</p>", unsafe_allow_html=True)
    st.markdown("<ul class='text'><li>专业：您的领域是什么？填上来！</li><li>年级：本科生、研究生还是博士生？搞定！</li><li>输出语言：想要哪种语言的内容？中文、英文，随您选！</li><li>学习风格：答几道小问题，帮我们更懂您！</li></ul>", unsafe_allow_html=True)
    st.markdown("<p class='text'>填好后点“提交”，系统会根据您的信息定制搜索建议和总结内容哦～</p>", unsafe_allow_html=True)

    st.markdown("<p class='step'>Step 2: 关键词搜索建议</p>", unsafe_allow_html=True)
    st.markdown("<p class='text'>在这里输入您的研究问题，系统会：</p>", unsafe_allow_html=True)
    st.markdown("<ul class='text'><li>给关键词建议：别再苦思冥想，多个关键词帮您搞定。</li><li>关键词定义：不懂关键词？系统帮您解释！</li></ul><br/>", unsafe_allow_html=True)

    st.markdown("<p class='step'>Step 3: 学术搜索板块</p>", unsafe_allow_html=True)
    st.markdown("<p class='text'>根据系统推荐的关键词，搜文献就是分分钟的事：</p>", unsafe_allow_html=True)
    st.markdown("<ul class='text'><li>输入关键词：搜索相关文献。</li><li>选择重点：亮点、理论、方法、分析、结论，想看啥就勾啥！</li><li>个性化总结：总结出您关心的内容，提取精华部分。</li><li>加入文献库：喜欢的文献直接收入囊中，以后再慢慢看！</li></ul><br/>", unsafe_allow_html=True)

    st.markdown("<p class='step'>Step 4: 文献库管理</p>", unsafe_allow_html=True)
    st.markdown("<p class='text'>已选文献板块里，随时可以：</p>", unsafe_allow_html=True)
    st.markdown("<ul class='text'><li>再次总结：随时回看、再总结，掌握文献内容不遗漏。</li></ul><br/>", unsafe_allow_html=True)

    st.markdown("<p class='subtitle'>使用小Tips</p>", unsafe_allow_html=True)
    st.markdown("<ul class='text'><li>关键词灵活调整：多试试关键词组合，找到最合适的内容！</li><li>精挑细选：放入文献库的文献，好好比较总结内容，选最适合您的。</li><li>关注重点随意选：学习、写作、演讲，选不同重点部分更高效！</li></ul>", unsafe_allow_html=True)

    st.markdown("<p class='text'>快来体验，看看它有多聪明吧！您的研究问题，就交给我们！</p>", unsafe_allow_html=True)

if 'keyword_results' not in st.session_state:
    st.session_state.keyword_results = None  # For storing keyword suggestions results

if 'df.data' not in st.session_state:
    st.session_state.search_results = pd.DataFrame()  # For storing search results in Tab 1

with st.expander("**💡关键词搜索建议**"):
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
        kws = json.loads(cleaned_keywords)
        st.session_state.keyword_results = kws  # Store in session state
    if st.session_state.keyword_results:
        for kw in st.session_state.keyword_results['keywords']:
            # annotated_text((kw['keyword'],"key word"))  # 标记关键词
            annotated_text((kw['keyword'], ""))  # Display keyword in boxed format
            # Add explanation in smaller font on a new line using st.markdown
            st.markdown(f"<p style='font-size: 14px;'>{kw['explanation']}</p>", unsafe_allow_html=True)
        

tab1, tab2 = st.tabs(["🔍学术搜索", "👓选出文献"])


with tab1:
    st.markdown('## ARXIV关键词搜索')
    # col1, col2 = st.columns([9, 1])
    # with col1:
    #     keyword = st.text_input("请输入你的关键词:", placeholder="请输入你的关键词:", value="", label_visibility='collapsed')
    # with col2:
    #     kw_submit = st.button("🔍", key='kw')
    
    # col3, col4 = st.columns([1,1])
    # history_papers = pd.DataFrame()
    
    # with col3:
    #     focus = st.multiselect(
    #         "你当前看文献关注的重点是什么",
    #         ["亮点","理论", "方法", "分析","结论"], placeholder="请选择")
    #     print(focus)

    keyword = st.text_input("请输入你的关键词:", placeholder="请输入")

    # Multi-select for focus areas
    focus = st.multiselect(
        "你当前看文献关注的重点是什么",
        ["亮点", "理论", "方法", "分析", "结论"], 
        placeholder="请选择"
    )

    kw_submit = st.button("提交进行搜索 🔍", key='kw')


    # 检查是否需要初始化或重置 df_data 和 selected_rows
    # if 'df_data' not in st.session_state or 'selected_rows' not in st.session_state:
    #     st.session_state.df_data = pd.DataFrame()
    #     st.session_state.selected_rows = pd.DataFrame()

    # 实现更新选中行的函数
    if keyword and kw_submit:
        st.session_state.df_data = search_summarize(keyword,major,role,language,focus,language,GPT_API_KEY)
    builder = GridOptionsBuilder.from_dataframe(st.session_state.df_data)
    builder.configure_selection('multiple', use_checkbox=True)
    # builder.configure_grid_options(domLayout='autoHeight', suppressRowTransform=False)
    

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

    # Configure the 'date' column with a smaller width
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

    if st.button("确认选中"):
        selected_rows = pd.DataFrame(grid_response['selected_rows'])
        if not selected_rows.empty:  # 使用.empty来检查DataFrame是否为空
            st.write("选中的标题:")
            for _, selected_row in selected_rows.iterrows():
                st.write(selected_row['Title'])
        else:
            st.write("没有选中的行。")

    # 调试输出当前选中的行数据
        st.write("当前选中的行数据:", selected_rows)



    
    