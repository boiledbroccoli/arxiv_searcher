import os,openai
from langchain import PromptTemplate
def summarize_all(papers4summarise,language,role,major,question,keyword,GPT_API_KEY,category = ''):
    # 该函数会在 page 里被召唤
    os.environ["OPENAI_API_KEY"] =  GPT_API_KEY
    
    with open('prompt_summarize_all.txt','r') as f:
        prompt_summarise_all   = f.read()
    prompt_summarise_all = PromptTemplate.from_template(prompt_summarise_all)
    if category == '':
        point6 = ''
    else:
        if category == '直觉型':
            category_format = "直觉型的学习者则喜欢创新，不喜欢重复而规律的事物。\n" \
            "直觉型学习者则擅长理解新的概念，他们对于抽象概念或数理公式容易适应，没有困扰。\n" \
            "直觉型学习者则喜欢以快速而创新的方式完成工作\n" \
            "直觉型学习者无法忍受需要填鸭式的大量记忆和冗长枯燥的计算\n" \
            "直觉型学习者面对枯燥的内容可能会感到无趣，需要提供所学相关的说明或理论解释"
        elif category == '感受型':
            category_format = "感受型的学习者偏好学习具体的事实，喜欢发觉事物间的关联或可能性\n" \
            "感受型的学习者通常喜欢用固有的方式去解决问题，不喜欢遇到复杂或是突发的状况，当课堂测验的内容超出所学的范围时，感受型学习者较 无法接受这种情况\n" \
            "感受型学习者对于细节会较有耐心去完成，而且擅长具体事实的记忆，以及实际操作(例如:实验室)的演练\n" \
            "感受型学习者比较实际且谨慎，较无法接受所学内容和真实世界是没有关连性的\n" \
            "感受型学习者能够发觉到学习与真实情境的关联性，这会让他们对于资讯的理解与记忆有较佳的成效。"
        point6 = f'6. 在呈现解结果的时候，请以{category}学习风格方便理解的语言和形式进行总结。{category}学习风格适应的学习方式:\n{category_format}'
    
    prompt_summarise_all = prompt_summarise_all.format(
        keyword = keyword,
        role = role,
        major = major,
        question = question,
        category = category,
        language = language,
        papers4summarise = papers4summarise,
        point6 = point6
    )
    client = openai.OpenAI()
    response = client.chat.completions.create(model='gpt-4',
                                              messages=[
                                                  {"role": "user", "content": prompt_summarise_all}]) # notice

    summary = response.choices[0].message.content
    return summary