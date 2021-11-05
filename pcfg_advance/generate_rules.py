import pickle
from progress.bar import Bar
import os
import re
import numpy as np
from utils import load_data
import string

FILE_NAME = 'yahoo'
# FILE_NAME = 'csdn'
FILE_PATH = f"./data/data_{FILE_NAME}.pkl"
TOTAL_COUNT = None

def generate_char_rule(passwords):
    char_rule = {}
    pattern = re.compile(r'([a-z]+)')
    bar = Bar(title="generate char rules", max=len(passwords))
    for password in passwords:
        chars = pattern.findall(password) # ['123', '321']
        for char in chars:
            if(char not in char_rule):
                char_rule[char] = 0
            char_rule[char] += 1
        bar.next()
    bar.finish()
    total_count = len(passwords)
    sorted_dict = sorted(char_rule.items(), key=lambda item: item[1], reverse=True)
    with open(f'./{FILE_NAME}/char_rule.txt', 'w', encoding='utf-8', errors='ignore') as f:
        for item in sorted_dict:
            key, value = item
            if(value <= 8):
                break
            value = float(value) / float(total_count)
            f.write(f'{key} {value:.5f}\n')


def generate_number_rule(passwords):
    number_rule = {}
    pattern = re.compile(r'(\d+)')

    bar = Bar(title="generate number rules", max=len(passwords))

    for password in passwords:
        numbers = pattern.findall(password) # ['123', '321']
        for number in numbers:
            if(number not in number_rule):
                number_rule[number] = 0
            number_rule[number] += 1
        bar.next()
    bar.finish()
    total_count = len(passwords)
    sorted_dict = sorted(number_rule.items(), key=lambda item: item[1], reverse=True)
    with open(f'./{FILE_NAME}/number_rule.txt', 'w', encoding='utf-8', errors='ignore') as f:
        for item in sorted_dict:
            key, value = item
            if(value <= 8):
                break
            value = float(value) / float(total_count)
            f.write(f'{key} {value:.5f}\n')


def generate_pattern_rule(passwords):
    pattern_rule = {}
    repattern = re.compile(r'([0-9]+|[a-z]+)')
    bar = Bar(title="generate pattern rules", max=len(passwords))
    for password in passwords:
        item_patterns = repattern.findall(password) # ['123', 'abc', '321']
        pattern = ''
        for itme_pattern in item_patterns:
            itme_pattern_key = 'L' if itme_pattern[0] in string.ascii_lowercase else 'D'
            itme_pattern_len = len(itme_pattern)
            pattern += '{},{},'.format(itme_pattern_key, itme_pattern_len)
        if(pattern not in pattern_rule):
            pattern_rule[pattern] = 0
        pattern_rule[pattern] += 1
        bar.next()
    bar.finish()

    total_count = len(passwords)
    sorted_dict = sorted(pattern_rule.items(), key=lambda item: item[1], reverse=True)
    with open(f'./{FILE_NAME}/pattern_rule.txt', 'w', encoding='utf-8', errors='ignore') as f:
        for item in sorted_dict:
            key, value = item
            key = key[:-1] # 去除末尾的逗号
            if(value <= 8):
                break
            value = float(value) / total_count
            f.write(f'{key} {value:.5f}\n')
            



def main():
    train_data, _ = load_data(FILE_PATH)

    generate_char_rule(train_data)
    generate_number_rule(train_data)
    generate_pattern_rule(train_data)

if __name__ == '__main__':
    main()