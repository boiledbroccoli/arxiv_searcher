def learning_style_calculator(data):
    ans_list = []
    for k in data:
        ans_list += [data[k]]
    count_a = ans_list.count('a')
    count_b = ans_list.count('b')

    score = count_b - count_a
    category = ''
    if score > 0: 
        category = '直觉型'
    elif score < 0:
        category = '感受型'
    return category