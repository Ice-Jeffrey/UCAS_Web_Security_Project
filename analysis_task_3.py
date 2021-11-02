from math import log
import re
import pickle


FILE_NAME = 'yahoo'
# FILE_NAME = 'csdn'
FILE_PATH = "./data/" + FILE_NAME + ".txt" # 453491
TOTAL_COUNT = None


def init_data():
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    global TOTAL_COUNT
    TOTAL_COUNT = len(lines)

    # print("Total Count =", TOTAL_COUNT)

    if("csdn" in FILE_PATH):
        passwords = ['#'.join(line.split(' # ')[1:-1]).strip()
                     for line in lines]
    else:
        passwords = [':'.join(line.split(':')[2:]).strip()
                    for line in lines]

    return passwords


# Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability).
lib_path = './lib/word_lib.txt'
# lib_path = './lib/pinyin_lib.txt'
words = open(lib_path, encoding='utf-8').read().split()
wordcost = dict((k, log((i + 1) * log(len(words)))) for i, k in enumerate(words))
maxword = max(len(x) for x in words)


# Vocabulary extraction
def infer_spaces(s):
    """Uses dynamic programming to infer the location of spaces in a string
    without spaces."""

    # Find the best match for the i first characters, assuming cost has
    # been built for the i-1 first characters.
    # Returns a pair (match_cost, match_length).
    def best_match(i):
        candidates = enumerate(reversed(cost[max(0, i - maxword):i]))
        return min((c + wordcost.get(s[i - k - 1:i], 9e999), k + 1) for k, c in candidates)

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


def word_analysis(passwords):
    word_lib = {}

    for password in passwords:
        # 只提取口令中的英文
        chars = re.split(r'[^A-Za-z]', password)
        while '' in chars:
            chars.remove('')
        
        for char in chars:
            word_list = infer_spaces(char)
            for word in word_list:
                word_lib[word] = word_lib.get(word, 0) + 1

    # 对得到的字典排序并输出
    sorted_lib = sorted(word_lib.items(), key = lambda kv:(kv[1], kv[0]), reverse=True) 
    print(sorted_lib)

    # 将排序后得到的列表保存在本地
    if 'pinyin' in lib_path:
        with open('./results/' + FILE_NAME + '_sorted_pinyin_lib.pkl', 'wb') as f:
            pickle.dump(sorted_lib, f, pickle.HIGHEST_PROTOCOL)
        f.close()
    else:
        with open('./results/' + FILE_NAME + '_sorted_word_lib.pkl', 'wb') as f:
            pickle.dump(sorted_lib, f, pickle.HIGHEST_PROTOCOL)
        f.close()

    return sorted_lib


def main():
    passwords = init_data()
    sorted_lib = word_analysis(passwords)


def show():
    if 'pinyin' in lib_path:
        with open('./results/' + FILE_NAME + '_sorted_pinyin_lib.pkl', 'rb') as f:
            sorted_lib = pickle.load(f)
        f.close()
    else:
        with open('./results/' + FILE_NAME + '_sorted_word_lib.pkl', 'rb') as f:
            sorted_lib = pickle.load(f)
        f.close()
    
    total = 0
    for element in reversed(sorted_lib):
        total += element[1]

    lines = []
    for element in sorted_lib:
        line = element[0]
        line += ' ' + str(element[1])
        line += ' ' + str(element[1] / total)
        line += ' ' + str(len(element[0]))
        lines.append(line)
    
    if 'pinyin' in lib_path:
        target_path = './results/' + FILE_NAME + '_pinyin.txt'
    else:
        target_path = './results/' + FILE_NAME + '_word.txt'
    with open(target_path, 'w') as f:
        f.write('\n'.join(lines))
    f.close()


if __name__ == "__main__":
    # main()
    show()