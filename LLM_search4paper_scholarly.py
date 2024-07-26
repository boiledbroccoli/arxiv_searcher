import os,openai,json,pandas as pd
from langchain_core.prompts import PromptTemplate

from langchain.llms.fake import FakeListLLM
from scholarly import scholarly


def search_scholarly(keyword,top = 5):
    if isinstance(keyword, list):
        keyword = ' '.join(keyword)
    search_query = scholarly.search_pubs(keyword)
    titles = []
    for i in range(top):
        x = next(search_query)
        x = x['bib']['title']
        titles.append(x)
    return titles
def search_pub_details(title):
    details = scholarly.search_single_pub(title)
    return details

def get_authors(author_list,tostr = True):
    
    if ~tostr:
        author_list = ''.join(author_list)
    return author_list

def format_result(text):
    results = []
    results.append({})
    results[0]['title'] = text['bib']['title']
    results[0]['authors'] = get_authors(text['bib']['author'])
    results[0]['citationCount'] = text['num_citations']
    results[0]['abstract'] = text['bib']['abstract']
    results[0]['pubyear'] = text['bib']['pub_year']
    try:
        results[0]['journal'] = text['bib']['venue']
    except Exception as e:
        results[0]['journal'] = ''
    try:
        results[0]['url'] = text['bib']['pub_url']
    except:
        results[0]['url'] = ''
    return results


# Define a wrapper function to use as a step in the chain
def semantic_scholar_search_step(keywords):
    keywords = json.loads(keywords)# notice: change
    keywords = keywords['keywords'] 
    all_results = []
    for keyword in keywords:
        titles = search_scholarly(keyword)
        for title in titles:
            result = search_pub_details(title)
            result = format_result(result)
            all_results += result
    return pd.DataFrame(all_results)


def search4paper(rq,field,GPT_API_KEY, model_type,prompt_kw = 'prompt_keywords.txt',temperature = 1):
    output_format = '{"keywords" : [COMBINATION1, COMBINATION2, ...] }'
    
    with open(prompt_kw,'r') as f:
        prompt_kw = f.read()
    prompt_kw = PromptTemplate.from_template(prompt_kw)
    prompt_kw = prompt_kw.format(field = field,
                                 research_question = rq,
                                 output_format = output_format)
    
    
    os.environ["OPENAI_API_KEY"] =  GPT_API_KEY
    client = openai.OpenAI()
    keywords = client.chat.completions.create(model=model_type,
                                              messages=[
                                                  {"role": "user", "content": prompt_kw }],
                                              temperature=temperature) # notice
    keywords = keywords.choices[0].message.content
    # print(type(keywords))
    # print(keywords)
    studies = semantic_scholar_search_step(keywords)
    # # delete the following two
    # responses = ['''{ "keywords" : [ "self-esteem and intimate relationships", "self-esteem impact on romantic relationships", "self-esteem influence on close relationships", "self-esteem and relationship satisfaction", "self-esteem and partner dynamics", "self-esteem and interpersonal relationships", "self-esteem effects on relationship quality" ] }''']
    # model = FakeListLLM(responses=responses)


    
    return studies
