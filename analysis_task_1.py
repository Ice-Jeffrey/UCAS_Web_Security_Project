# Length & Components analysis for token

from collections import Counter
import os
import pickle
import re
from pyecharts import options as opts
from pyecharts.charts import Page, Pie

def show_pie(title, labels, values):
    pie = (
            Pie()
            .add("", [list(z) for z in zip(labels, values)], radius=["40%","75%"])
            .set_global_opts(title_opts=opts.TitleOpts(title=title), 
                            legend_opts=opts.LegendOpts(
                                orient="vertical", pos_top="5%", pos_right="2%"  # 左面比例尺
                                ),
                            )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
        )
    pie.render(title + '.html')

    
FILE_NAME = 'yahoo'
# FILE_NAME = 'csdn'
FILE_PATH = "./" + FILE_NAME + ".txt" # 453491
TOTAL_COUNT = None


def init_data():
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    global TOTAL_COUNT
    TOTAL_COUNT = len(lines)

    print("Total Count =", TOTAL_COUNT)

    if("csdn" in FILE_PATH):
        passwords = ['#'.join(line.split('#')[1:-1]).strip()
                     for line in lines]
    else:
        passwords = [':'.join(line.split(':')[2:]).strip()
                    for line in lines]

    return passwords


def components_analysis(passwords):

    # [1] 数字、小写字母、大写字母、其它字符('ɾɱ', )
    # [2894599, 750370, 30543, 2756]
    # ['45.03%', '11.67%', '0.48%', '0.04%']

    # [2] 数字+小写字母，数字+大写字母，数字+其它字符，小写+大写，小写+其它，大写+其它
    # [2286902, 146644, 39539, 14870, 28155, 1489]
    # ['35.57%', '2.28%', '0.62%', '0.23%', '0.44%', '0.02%']

    # [3] 数字+小写字母+大写字母，数字+小写字母+其它字符，小写+大写+其它
    # [73200, 131976, 3894]
    # ['1.14%', '2.05%', '0.06%']

    infos_1 = [0] * 4
    infos_2 = [0] * 6
    infos_3 = [0] * 3

    for i, password in enumerate(passwords):
        if(re.match(r'[0-9]+$', password)):  # 仅数字
            infos_1[0] += 1
        elif(re.match(r'[a-z]+$', password)):  # 仅小写字母
            infos_1[1] += 1
        elif(re.match(r'[A-Z]+$', password)):  # 仅大写字母
            infos_1[2] += 1
        elif(re.match(r'[^0-9a-zA-Z]+$', password)):  # 仅其它
            infos_1[3] += 1
        elif(re.match(r'[0-9a-z]+$', password)):  # 数字+小写字母 's12345'
            infos_2[0] += 1
        elif(re.match(r'[0-9A-Z]+$', password)):  # 数字+大写字母 'ZKL229'
            infos_2[1] += 1
        elif(re.match(r'[^a-zA-Z]+$', password)):  # 数字+其它字符 '@3202379'
            infos_2[2] += 1
        elif(re.match(r'[a-zA-Z]+$', password)):  # 小写+大写 'FireTM'
            infos_2[3] += 1
        elif(re.match(r'[^0-9A-Z]+$', password)):  # 小写+其它 'yulingkong!!'
            infos_2[4] += 1
        elif(re.match(r'[^0-9a-z]+$', password)):  # 大写+其它 'Q!W@E'
            infos_2[5] += 1
        elif(re.match(r'[0-9a-zA-Z]+$', password)):  # 数字+小写字母+大写字母 'Lwxss21cn'
            infos_3[0] += 1
        elif(re.match(r'[^A-Z]+$', password)):  # 数字+小写字母+其它字符 '1900@csdn'
            infos_3[1] += 1
        elif(re.match(r'[^0-9]+$', password)):  # 小写+大写+其它 'i"mAgilent'
            infos_3[2] += 1

        if(i % 1000000 == 0):
            print(i)
    for count, name in zip(infos_1, ['[仅]数字', '[仅]小写字母', '[仅]大写字母', '[仅]其它字符']):
        print("{} = {} 个 比例 = {}%".format(
            name, count, round(count / TOTAL_COUNT * 100, 2)))

    for count, name in zip(infos_2, ['数字+小写字母', '数字+大写字母', '数字+其它字符', '小写+大写', '小写+其它', '大写+其它']):
        print("{} = {} 个 比例 = {}%".format(
            name, count, round(count / TOTAL_COUNT * 100, 2)))

    for count, name in zip(infos_3, ['数字+小写字母+大写字母', '数字+小写字母+其它字符', '小写+大写+其它']):
        print("{} = {} 个 比例 = {}%".format(
            name, count, round(count / TOTAL_COUNT * 100, 2)))


def length_analysis(title, passwords):
    
    length_dict = {}

    for password in passwords:
        length = len(password)

        if(length == 0): 
            continue

        if(length in length_dict.keys()):
            length_dict[length] += 1
        else:
            length_dict[length] = 1
    sorted_dict = sorted(length_dict.items(), key=lambda item: item[0])
    
    show_pie(title, [item[0] for item in sorted_dict], [item[1] for item in sorted_dict])

def topN(title, lst, N=10):
    counter = Counter(lst)
    topn = counter.most_common(N)
    print('\n最常见的十种结构是（A代表字母，N代表数字，O代表其它字符）：')

    labels = []
    values = []
    for i in range(len(topn)):
        labels.append(topn[i][0])
        values.append(topn[i][1])
        if len(topn[i][0]) <= 6:
            print(topn[i][0], '\t\t', topn[i][1], '\t', round(
                int(topn[i][1])/TOTAL_COUNT*100, 2), '%')
        else:
            print(topn[i][0], '\t', topn[i][1], '\t', round(
                int(topn[i][1])/TOTAL_COUNT*100, 2), '%')
    show_pie('topn_' + title, labels, values)

def pattern_analysis(passwords):
    patterns = []
    patterns_advance = []
    for i, password in enumerate(passwords):
        pattern = re.sub(r'[a-zA-Z]', 'A', password, count=0)
        pattern = re.sub(r'[^0-9a-zA-Z]', 'O', pattern, count=0)
        pattern = re.sub(r'[0-9]', 'N', pattern, count=0)

        pattern_advance = re.sub(r'[N]+', 'N', pattern, count=0)
        pattern_advance = re.sub(r'[A]+', 'A', pattern_advance, count=0)
        pattern_advance = re.sub(r'[O]+', 'O', pattern_advance, count=0)

        patterns.append(pattern)
        patterns_advance.append(pattern_advance)

        if(i % 1e6 == 0):
            print(i)

    return patterns, patterns_advance


def main():

    passwords = init_data()

    # 组成元素分析
    """
        # [1] 数字、小写字母、大写字母、其它字符('ɾɱ', )
        # [2894599, 750370, 30543, 2756]
        # ['45.03%', '11.67%', '0.48%', '0.04%']

        # [2] 数字+小写字母，数字+大写字母，数字+其它字符，小写+大写，小写+其它，大写+其它
        # [2286902, 146644, 39539, 14870, 28155, 1489]
        # ['35.57%', '2.28%', '0.62%', '0.23%', '0.44%', '0.02%']

        # [3] 数字+小写字母+大写字母，数字+小写字母+其它字符，小写+大写+其它
        # [73200, 131976, 3894]
        # ['1.14%', '2.05%', '0.06%']
    """
    # components_analysis(passwords)

    components = ['数字', '小写字母', '大写字母', '其它字符', '数字+小写字母', '数字+大写字母',
                   '数字+其它字符', '小写+大写', '小写+其它', '大写+其它', '数字+小写字母+大写字母', 
                   '数字+小写字母+其它字符', '小写+大写+其它']
    values = [2894599, 750370, 30543, 2756, 2286902, 146644, 39539, 14870, 28155, 1489, 73200, 131976, 3894]
    show_pie(FILE_NAME + '组成元素分析', components, values)

    """[长度分析]
    """
    length_analysis(FILE_NAME + '长度分析', passwords)

    # 构成模式
    if not os.path.exists('patterns.pkl'):
        patterns, patterns_advance = pattern_analysis(passwords)
        with open('patterns.pkl', 'wb') as f:
            pickle.dump((patterns, patterns_advance), f)
    else:
        with open('patterns.pkl', 'rb') as f:
            patterns, patterns_advance = pickle.load(f)

    topN(FILE_NAME + '构成模式_base', patterns)
    topN(FILE_NAME + '构成模式_advance', patterns_advance)


if __name__ == '__main__':
    main()
