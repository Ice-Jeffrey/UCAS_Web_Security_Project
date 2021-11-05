import pickle
import re
from math import log

FILE_NAME = 'csdn'
# FILE_NAME = 'yahoo'

lib_path = './lib/word_lib.txt'
# Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability).
eng_words = open(lib_path, encoding='utf-8').read().split()
eng_wordcost = dict((k, log((i + 1) * log(len(eng_words)))) for i, k in enumerate(eng_words))
eng_maxword = max(len(x) for x in eng_words)

lib_path = './lib/pinyin_lib.txt'
py_words = open(lib_path, encoding='utf-8').read().split()
py_wordcost = dict((k, log((i + 1) * log(len(py_words)))) for i, k in enumerate(py_words))
py_maxword = max(len(x) for x in py_words)


# Vocabulary extraction
def infer_spaces(s, tag):
    """Uses dynamic programming to infer the location of spaces in a string
    without spaces."""

    # Find the best match for the i first characters, assuming cost has
    # been built for the i-1 first characters.
    # Returns a pair (match_cost, match_length).
    def best_match(i):
        if tag == 'eng':
            candidates = enumerate(reversed(cost[max(0, i - eng_maxword):i]))
            return min((c + eng_wordcost.get(s[i - k - 1:i], 9e999), k + 1) for k, c in candidates)
        else:
            candidates = enumerate(reversed(cost[max(0, i - py_maxword):i]))
            return min((c + py_wordcost.get(s[i - k - 1:i], 9e999), k + 1) for k, c in candidates)

    # Build the cost array.
    cost = [0]
    for i in range(1, len(s) + 1):
        c, k = best_match(i)
        cost.append(c)

    # Backtrack to recover the minimal-cost string.
    out = []
    i = len(s)
    while i > 0:
        c, k = best_match(i)
        assert c == cost[i]
        out.append(s[i - k:i])
        i -= k

    return reversed(out)


def word_analysis(passwords, tag):
    word_lib = {}

    for password in passwords:
        # 只提取口令中的英文
        chars = re.split(r'[^A-Za-z]', password)
        while '' in chars:
            chars.remove('')
        
        for char in chars:
            word_list = infer_spaces(char, tag)
            for word in word_list:
                word_lib[word] = word_lib.get(word, 0) + 1

    # 对得到的字典排序并输出
    sorted_lib = sorted(word_lib.items(), key = lambda kv:(kv[1], kv[0]), reverse=True) 
    # print(sorted_lib)

    return sorted_lib

    
def main():
    with open('../data/data_' + FILE_NAME + '.pkl', 'rb') as f:
        passwords = pickle.load(f)[0]

    pinyin_lib = word_analysis(passwords, tag='py')
    word_lib = word_analysis(passwords, tag='eng')

    total = 0
    total_lib = pinyin_lib + word_lib
    for element in reversed(total_lib):
        total += element[1]

    total_dic = {}
    for element in total_lib:
        key, value = element[0], element[1]
        total_dic[key] = total_dic.get(key, 0) + value 
    
    sorted_list = sorted(total_dic.items(), key = lambda kv:(kv[1], kv[0]), reverse=True) 

    lines = []
    for item in sorted_list:
        line = item[0]
        line += ' ' + str(item[1] / total)
        lines.append(line)
    # print(lines)
    # exit()
    
    target_path = './results/' + FILE_NAME + '_lib_pcfg.txt'
    with open(target_path, 'w') as f:
        f.write('\n'.join(lines))
    f.close()


if __name__ == "__main__":
    main()
