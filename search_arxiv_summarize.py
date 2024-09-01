import pandas as pd, os
import arxiv
import streamlit as st
import re
import openai


# 定义映射字典
translations = {
    "心理学": "Psychology",
    "本科生": "Undergraduate",
    "研究生": "Graduate",
    "中文": "Chinese",
    "英文": "English",
    "直观型": "Intuitive",
    "感性": "Sensing",
    "亮点": "Highlights",
    "理论框架": "Theoretical Framework",
    "方法": "Methods",
    "分析": "Analysis",
    "结论": "Results",
}

def translate(inputs):
    return [translations.get(item, item) for item in inputs]

def generate_summary(abstract, major, role, language, category, focus):
    major = translations.get(major, major)
    role = translations.get(role, role)
    language = translations.get(language, language)
    category = translations.get(category, category)

    prompt = f'''You are tasked with analyzing an abstract to tailor insights to students majoring in {major}. Here is the abstract: "{abstract}"\n\n'''
    prompt += f'Your explanations should be suited to a {category.lower()} cognitive style and the understanding level of a {role.lower()}, and should be presented in {language}.\n\n'''

    focus_dict = {
        'Highlights': "Identify and discuss the key points and innovative aspects of the research relevant to the focus areas.",
        'Theoretical Framework': "Outline the theoretical underpinnings and hypotheses of the study, providing explanations suited to the reader's subject and grade level.",
        'Methods': "Describe the research design and experimental methods used in the study. Focus on the approach and rationale for the chosen methods, ensuring clarity and relevance to the specified focus areas.",
        'Analysis': "Detail the data analysis techniques employed in the research. Emphasize how these methods contribute to the findings, tailored to the user's understanding and interests.",
        'Results': "Summarize the main outcomes and conclusions of the study, highlighting how they address the research questions and impact the focus areas."
    }

    for area in focus:
        if area in focus_dict:
            prompt += f"{focus_dict[area]}\n"
    
    prompt += '''The analysis must strictly use the following section names only: Highlights, Theoretical Framework, Methods, Analysis, Results. 
    Do not use any other section names or variations.

    Your analysis will be structured into the following sections, each corresponding to a focus area you specified. The output will be formatted in a simplified JSON style with section headers in English and content in the specified language. Below is an example of the format. The section names must match exactly as specified:

    Example Format:
    {
        "Highlights": "Your detailed explanation for the Highlights section tailored to the specified cognitive style and understanding level.",
        "Theoretical Framework": "Your detailed explanation for the Theoretical Framework section.",
        "Methods": "Your detailed explanation for the Methods section.",
        "Analysis": "Your detailed explanation for the Analysis section.",
        "Results": "Your detailed explanation for the Results section."
    }
    
    Note: The sections generated will align with the focus areas you have specified (e.g., Highlights, Theoretical Framework, Methods, Analysis, Results). This example shows the format only; the content should be generated accordingly, without changing section names.'''

    return prompt

# def clean_text(text):
#     """Remove formatting characters like **, \n and extra spaces."""
#     text = re.sub(r'\*\*', '', text)  # Remove double asterisks
#     text = re.sub(r'\n', ' ', text)  # Replace newlines with spaces
#     text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
#     return text.strip()

def extract_section(text, section_name):
    pattern = rf'\"{section_name}\": \"(.*?)\"'
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1) if match else ""


def search_summarize(keyword,major,role,language,focus,category,GPT_API_KEY):
    # 该函数会在 page 里被召唤
    os.environ["OPENAI_API_KEY"] =  GPT_API_KEY

    client = arxiv.Client()
    search = arxiv.Search(
    query = keyword,
    max_results = 3,
    sort_by = arxiv.SortCriterion.SubmittedDate
    )

    results = client.results(search)

    translated_focus = translate(focus)

    data = []

    for result in results:
        client = openai.OpenAI()
        clean_summary = result.summary.replace('\n', ' ')
        print(clean_summary)
        # def generate_summary(abstract, major, role, language, category, focus):
        prompt_summary = generate_summary(result.summary,major,role,language,category,translated_focus)
        response = client.chat.completions.create(model='gpt-4o',
                                              messages=[
                                                  {"role": "user", "content": prompt_summary}]) # notice

        analysis = response.choices[0].message.content
        print(analysis)
        analysis_dict = {
            "Highlights": extract_section(analysis, "Highlights"),
            "Theoretical Framework": extract_section(analysis, "Theoretical Framework"),
            "Methods": extract_section(analysis, "Methods"),
            "Analysis": extract_section(analysis, "Analysis"),
            "Results": extract_section(analysis, "Results")
        }

        filtered_analysis_dict = {key: value for key, value in analysis_dict.items() if key in translated_focus}
        print("filtered_analysis_dict",filtered_analysis_dict)
        print("translated_focus",translated_focus)

        data.append({
            "Title": result.title,
            "Abstract": clean_summary,
            "Date": result.published.strftime('%Y-%m-%d'),
            **filtered_analysis_dict
        })

    df = pd.DataFrame(data)
    return df