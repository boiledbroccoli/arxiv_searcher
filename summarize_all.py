import os
def summarize_all(papers,GPT_API_KEY,category = ''):
    # 该函数会在 page 里被召唤
    os.environ["OPENAI_API_KEY"] =  GPT_API_KEY
    
    summary = 'hahahha'
    return summary