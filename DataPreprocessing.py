import os
import io
from numpy import character
import pandas as pd
from pypinyin import lazy_pinyin


def word_dataset_processing():
    # 处理雅虎数据集
    yahoo_dir = './raw_data/plaintxt_yahoo/plaintxt_yahoo.txt'
    with open(yahoo_dir, 'r', encoding='unicode_escape') as f:
        lines = f.readlines()
        header = lines[3070]
        datalines = lines[3072: 3072+453491+1]

        with open('./data/yahoo.txt', 'w', encoding='utf-8') as wfile:
            wfile.writelines(datalines)
        wfile.close()
    f.close()
    
    # 处理CSDN数据集
    csdn_dir = 'D:\\MyStudy\\UCAS\\Web_Security\\raw_data\\plaintxt_csdn\\www.csdn.net_utf-8.txt'
    with open(csdn_dir, 'r', encoding='utf-8') as f:
        lines = f.readlines()

        with open('./data/csdn.txt', 'w', encoding='utf-8') as wfile:
            wfile.writelines(lines)
        wfile.close()
    f.close()


def pinyin_corpus_processing():
    # 处理汉语拼音数据集
    excel = pd.read_excel('./lib/CorpusWordlist.xls', header=None, index_col=None)
    sheet = excel.iloc[7:, 1:3]
    # print(sheet)

    pinyin_lib = {}
    for i in range(sheet.shape[0]):
        character = sheet.iloc[i, 0]
        key = ''.join(lazy_pinyin(character))
        value = sheet.iloc[i, 1]
        pinyin_lib[key] = pinyin_lib.get(key, 0) + value

    sorted_lib = sorted(pinyin_lib.items(), key = lambda kv:(kv[1], kv[0]), reverse=True) 
    
    lines = [key for key, _ in sorted_lib]
    
    with open('./lib/pinyin_lib.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def main():
    # word_dataset_processing()
    pinyin_corpus_processing()


if __name__ == "__main__":
    main()