import pickle
from progress.bar import Bar
import os
import re
import numpy as np

FILE_NAME = 'yahoo'
# FILE_NAME = 'csdn'
FILE_PATH = "./data/" + FILE_NAME + ".txt"
TOTAL_COUNT = None

# 读取密码，统计总数
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


def _filter_data(passwords):
    filtered_data = []
    bar = Bar(max=len(passwords))
    for password in passwords:
        length = len(password)
        # 数字+小写字母 's12345'
        if(length >= 6 and length <= 12 and re.match(r'[0-9a-z]+$', password)):
            filtered_data.append(password)
        bar.next()
    bar.finish()
    return filtered_data


def _split_data(data, count=50000):
    length = len(data)
    indexes = list(range(length))
    indexes = np.random.permutation(indexes)

    train_indexes = indexes[:-count]
    test_indexes = indexes[-count:]

    train_data = [data[i] for i in train_indexes]
    test_data = [data[i] for i in test_indexes]

    return train_data, test_data


def filter_split_data(passwords):
    # 构成模式
    data_save_path = './data/data_{}.pkl'.format(FILE_NAME)
    if not os.path.exists(data_save_path):
        filtered_data = _filter_data(passwords)
        train_data, test_data = _split_data(filtered_data)
        with open(data_save_path, 'wb') as f:
            pickle.dump((train_data, test_data), f)
    else:
        with open(data_save_path, 'rb') as f:
            train_data, test_data = pickle.load(f)

    return train_data, test_data

def main():
    passwords = init_data()

    train_data, test_data = filter_split_data(passwords)

if __name__ == '__main__':
    main()
