import os,openai,json, time,pandas as pd
import streamlit as st

def prompt_kw_generation(research_question, language):

    prompt_kw = f"""
    ### 
    Role
    You are a specialized academic professor assistant.

    ### 
    Task
    The user focuses on the research question: {research_question}. Your task is to identify highly relevant and specific keyword phrases in English, based on the provided research question. The explanations for these keyword phrases should be provided in the language specified by the input variable {language} and should be sufficiently detailed to guide effective academic research. Follow these steps to ensure comprehensive coverage:

    1. **Understand the Question**: Interpret the research question to grasp its core components, objectives, and the relationships between key concepts thoroughly.
      
    2. **Identify Key Concepts and Relationships**: Decompose the question into main concepts, subtopics, and the relationships between them, focusing on dimensions such as methodologies, applications, historical context, and related studies.

    3. **Generate Keyword Phrases**: Create specific, information-rich English keyword phrases that reflect the core concepts and their interconnections (e.g., “AI-driven personalized persuasion”). Ensure these phrases capture the multidimensional aspects of the research question and are suitable for in-depth scholarly article searches.

    4. **Review and Refine**: Evaluate the keyword phrases to ensure they are precise, contextually relevant, and offer substantial information directly linked to the research question.

    5. **Final Evaluation**: Select the top 3 most useful and detailed English keyword phrases and provide a comprehensive explanation for each, in the language specified by {language}.

    The output should be in JSON format, providing only the final three keyword phrases with their explanations, structured for clear and concise data representation. Do not include the intermediate steps. Here’s the format for your output.


    ### 
    Output Format

    ```json
    {{
      "keywords": [
        {{
          "keyword": "keyword phrase 1",
          "explanation": "Detailed explanation of why keyword phrase 1 is critical: [Provide an in-depth analysis of what kind of content or research might be found using this phrase and how it can contribute to the user's research. The explanation should adapt to either English or Chinese based on the specified language.]"
        }},
        {{
          "keyword": "keyword phrase 2",
          "explanation": "Detailed explanation of why keyword phrase 2 is critical: [Provide an in-depth analysis of what kind of content or research might be found using this phrase and how it can contribute to the user's research. The explanation should adapt to either English or Chinese based on the specified language.]"
        }},
        {{
          "keyword": "keyword phrase 3",
          "explanation": "Detailed explanation of why keyword phrase 3 is critical: [Provide an in-depth analysis of what kind of content or research might be found using this phrase and how it can contribute to the user's research. The explanation should adapt to either English or Chinese based on the specified language.]"
        }}
      ]
    }}
    ```"""
    
    return prompt_kw


def keyword_generator(research_question, language, GPT_API_KEY,model_type="gpt-4"):
    # 该函数会在 page 里被召唤
    os.environ["OPENAI_API_KEY"] =  GPT_API_KEY
    with st.status("开始上传研究问题", expanded=True) as status:
        st.write("问题上传中...")
    # 以下是丢给 chatGPT 生成 summary 的代码
        prompt_kw = prompt_kw_generation(research_question,language)
        print(prompt_kw)
        status.update(label="关键词生成中...")
        st.write("关键词生成中...")
        client = openai.OpenAI()
        keywords = client.chat.completions.create(model=model_type,
                                                  messages=[
                                                      {"role": "user", "content": prompt_kw }]) # notice
        status.update(label="整合数据中...", expanded=True)
        st.write("整合数据...")

    time.sleep(1)

    status.update(label="成功🎉", expanded=False)    
    return keywords.choices[0].message.content
