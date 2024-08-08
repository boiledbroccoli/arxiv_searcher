import pandas as pd, os

def search_summarize(keyword,focus,expected_language,GPT_API_KEY):
    # 该函数会在 page 里被召唤
    os.environ["OPENAI_API_KEY"] =  GPT_API_KEY

    
    papers = [{'title' : 'AAAAAA','author': 'xx','year':'2024','summary': '_____'},
              {'title' : 'BBBBB','author': 'xx','year':'2024','summary': '_____'},
              {'title' : 'CCCC','author': 'xx','year':'2024','summary': '_____'},]
    papers = pd.DataFrame(papers)
    return papers

