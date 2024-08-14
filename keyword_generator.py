import os,openai,json,pandas as pd
from langchain_core.prompts import PromptTemplate

def keyword_generator(research_question, GPT_API_KEY,temperature = 0, model_type="gpt-4"):
    # 该函数会在 page 里被召唤
    os.environ["OPENAI_API_KEY"] =  GPT_API_KEY

    # 以下是丢给 chatGPT 生成 summary 的代码
    with open('prompt_keywords.txt','r') as f:
        prompt_kw = f.read()
    prompt_kw = PromptTemplate.from_template(prompt_kw)
    
    # output_format = '{"keywords" : [COMBINATION1, COMBINATION2, ...] }' #notice: 
    
    prompt_kw = prompt_kw.format(research_question = research_question)
    # notice: 目前设置的可变更的地方有两个：research_question 
    
    client = openai.OpenAI()
    keywords = client.chat.completions.create(model=model_type,
                                              messages=[
                                                  {"role": "user", "content": prompt_kw }],
                                              temperature=temperature) # notice
    keywords = {'AA':'explanation for Why A',
                'BB':'explanation for Why B'} # notice: 显示用，可删除
    return keywords