import os,openai
# from langchain import PromptTemplate
def get_focus_def(focus) -> list:
    dict_def = {
        '理论': '   - 理论：研究中用于解释现象或指导研究的基本概念和原理。',
        '亮点': '   - 亮点：研究中最重要的发现或贡献，通常是其创新性或独特性所在。',
        '方法': '   - 方法：用于收集和分析数据的具体步骤和技术。',
        '分析': '   - 分析:对数据进行解读和评估，以得出研究结果。',
        '结论': '   - 研究所得到的最终结果或发现，总结了研究的意义和影响。'
    }
    focus_def = ''
    for f in focus:
        focus_def += dict_def[f]
    return focus_def




def summarize_all(papers4summarise,language,role,major,question,focus,GPT_API_KEY,category = ''):
    # 该函数会在 page 里被召唤
    os.environ["OPENAI_API_KEY"] =  GPT_API_KEY
    
    focus_def = get_focus_def(focus)
    if len(focus) > 1:
        focus = '、'.join(focus)
    else:
        focus = focus[0]
    with open('prompt_summarize_all.txt','r') as f:
        prompt_summarise_all   = f.read()
    # prompt_summarise_all = PromptTemplate.from_template(prompt_summarise_all)
    if category == '':
        point4 = ''
    else:
        category += "的学习风格"
        if  '直觉型' in category:
            category_format = \
            "   - 直觉型的学习者喜欢创新，不喜欢重复而规律的事物。\n"\
            "   - 直觉型学习者擅长理解新的概念，对于抽象概念或数理公式容易适应，没有困扰。\n"\
            "   - 直觉型学习者喜欢以快速而创新的方式完成工作。\n"\
            "   - 直觉型学习者无法忍受需要填鸭式的大量记忆和冗长枯燥的计算。\n"\
            "   - 直觉型学习者面对枯燥的内容可能会感到无趣，需要提供所学相关的说明或理论解释。"
        elif '感受型' in category :
            category_format = \
            "   - 感受型的学习者偏好学习具体的事实，喜欢发觉事物间的关联或可能性\n"\
            "   - 感受型的学习者通常喜欢用固有的方式去解决问题，不喜欢遇到复杂或是突发的状况，当课堂测验的内容超出所学的范围时，感受型学习者较 无法接受这种情况\n"\
            "   - 感受型学习者对于细节会较有耐心去完成，而且擅长具体事实的记忆，以及实际操作的演练.\n"\
            "   - 感受型学习者比较实际且谨慎，较无法接受所学内容和真实世界是没有关连性的。\n"\
            "   - 感受型学习者能够发觉到学习与真实情境的关联性，这会让他们对于资讯的理解与记忆有较佳的成效。"
        point4 = f'4. 根据{category}，使用适合该风格的语言和形式呈现总结。{category}的具体表现形式为:\n{category_format}'
    
    # if category != '':
    #     link = '，以及'
    # else:
    #     link = ''
    # prompt_summarise_all = prompt_summarise_all.format(
    #     role = role,
    #     major = major,
    #     focus  = focus,
    #     focus_def = focus_def,
    #     question = question,
    #     category = category,
    #     language = language,
    #     papers4summarise = papers4summarise,
    #     point4 = point4
    # )
    prompt_summarise_all = eval('f' + repr(prompt_summarise_all))
    print(prompt_summarise_all)
    client = openai.OpenAI()
    response = client.chat.completions.create(model='gpt-4o',
                                              messages=[
                                                  {"role": "user", "content": prompt_summarise_all}]) # notice

    summary = response.choices[0].message.content
    return summary