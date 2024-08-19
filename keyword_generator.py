import os,openai,json,pandas as pd
from langchain_core.prompts import PromptTemplate

def prompt_kw_generation(research_question, major, language):

    prompt_kw = f"""
    You are a specialized academic professor in {major}.

    The user focuses on the research question: {research_question}. Your task is to identify highly relevant and specific keywords in English, based on the provided research question. The explanations for these keywords should be provided in the language specified by the input variable {language} and should be sufficiently detailed to guide effective academic research. Follow these steps to ensure comprehensive coverage:

    1. Understand the Question: Interpret the research question to grasp its core components and objectives thoroughly.
    2. Identify Key Concepts: Decompose the question into main concepts and subtopics, focusing on dimensions such as methodologies, applications, historical context, and related studies.
    3. Generate Keywords: Identify specific, information-rich English keywords from the main concepts, suitable for in-depth scholarly article searches and research exploration.
    4. Review and Refine: Evaluate the keywords to ensure they are precise, relevant, and offer substantial information directly linked to the research question.
    5. Final Evaluation: Select the top 3 most useful and detailed English keywords and provide a comprehensive explanation for each, in the language specified by {language}.

    The output should be in JSON format, providing only the final three keywords with their explanations, structured for clear and concise data representation. Do not include the intermediate steps. Here’s the format for your output:

    ```json
    {{
      "keywords": [
        {{
          "keyword": "keyword1",
          "explanation": "Detailed explanation of why keyword1 is critical: [Provide an in-depth analysis of what kind of content or research might be found using this keyword and how it can contribute to the user's research. The explanation should adapt to either English or Chinese based on the specified language.]"
        }},
        {{
          "keyword": "keyword2",
          "explanation": "Detailed explanation of why keyword2 is critical: [Provide an in-depth analysis of what kind of content or research might be found using this keyword and how it can contribute to the user's research. The explanation should adapt to either English or Chinese based on the specified language.]"
        }},
        {{
          "keyword": "keyword3",
          "explanation": "Detailed explanation of why keyword3 is critical: [Provide an in-depth analysis of what kind of content or research might be found using this keyword and how it can contribute to the user's research. The explanation should adapt to either English or Chinese based on the specified language.]"
        }}
      ]
    }}"""
    
    return prompt_kw


def keyword_generator(research_question, major, language, GPT_API_KEY,model_type="gpt-4"):
    # 该函数会在 page 里被召唤
    os.environ["OPENAI_API_KEY"] =  GPT_API_KEY

    # 以下是丢给 chatGPT 生成 summary 的代码
    prompt_kw = prompt_kw_generation(research_question, major,language)
    print(prompt_kw)
    
    client = openai.OpenAI()
    keywords = client.chat.completions.create(model=model_type,
                                              messages=[
                                                  {"role": "user", "content": prompt_kw }]) # notice
    # keywords = {'AA':'explanation for Why A',
    #             'BB':'explanation for Why B'} # notice: 显示用，可删除
    return keywords.choices[0].message.content
