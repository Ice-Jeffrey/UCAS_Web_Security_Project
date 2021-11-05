from tqdm import tqdm
import itertools
import gc
import os
from test import test
from generate_rules import FILE_NAME

# FILE_NAME = 'yahoo'
FILE_NAME = 'csdn'
FILE_PATH = f"./data/data_{FILE_NAME}.pkl"

def print_lst(lst):

    max_size=max(max(len(j) for j in i) for i in lst)
    max_col=max(len(i) for i in lst)
    
    for i in range(len(lst)):
        for j in range(max_col):
            print(eval("'{: ^"+str(max_size)+"}'.format(lst[i][j] if j < len(lst[i]) else '')"),end='|')
        print('\n'+'='*((max_size+1)*max_col))


class PCFG:
    def __init__(self,data_dir=f'./{FILE_NAME}', 
                # char_rule_filename='char_rule.txt', 
                char_rule_filename='char_lib.txt', 
                number_rule_filename='number_rule.txt',
                pattern_rule_filename='pattern_rule.txt'):

        char_rule = self.get_data(data_dir, char_rule_filename)
        number_rule = self.get_data(data_dir, number_rule_filename)
        pattern_rule = self.get_data(data_dir, pattern_rule_filename)
        self.pattern_rules = [ self._str2tuple(rule) for rule in pattern_rule]

        self.rule_char = self.get_rule(char_rule) # 长度与内容的映射
        self.rule_number = self.get_rule(number_rule)

        self.limit = 1000

        with open('res.txt', 'a', encoding='utf-8') as f:
            f.write('{}, {}, {}, result = '.format(FILE_NAME, char_rule_filename, number_rule_filename))
        with open('info.txt', 'a', encoding='utf-8') as f:
            f.write('{}, {}, {}, infos:\n'.format(FILE_NAME, char_rule_filename, number_rule_filename))

    def _str2tuple(self, rule):
        pattern_str, p = rule
        pattern_lst = pattern_str.split(',')
        res = []
        for i in range(0, len(pattern_lst), 2):
            res.append((pattern_lst[i], int(pattern_lst[i+1])))
        res.append(p)
        return res

    def get_data(self, data_dir, filename):
        with open(os.path.join(data_dir, filename), 'r') as f:
            lines = f.readlines()
        return [line.strip().split(' ') for line in lines if not line.isspace()]

    def get_rule(self, items):
        rule = {}
        for item in items:
            content = str(item[0]) # 内容
            p = float(item[1]) # 概率
            length = len(content) # 长度

            if(length not in rule):
                rule[length] = []

            rule[length].append([content, p])
        return rule

    def generate(self):
        res = []
        for rule in tqdm(self.pattern_rules):
            patterns = rule[:-1]
            if(FILE_NAME == 'yahoo'):
                if(len(patterns) == 3): self.limit = 100
                elif(len(patterns) < 3): self.limit = 1000
                else: continue
            elif(FILE_NAME == 'csdn'):
                if(len(patterns) == 1): self.limit = 1000
                elif(len(patterns) <= 3): self.limit = 100
                else: continue
            p = rule[-1]
            gen_pwds = self._generate_by_pattern(patterns, p)
            res.extend(gen_pwds)

            del gen_pwds
            gc.collect()
        res.sort(key=lambda item : item[1], reverse=True)
        return res

    def _generate_by_pattern(self, patterns, p):
        pattern = patterns[0]
        key = pattern[0]
        value = pattern[1]
        try:
            if key == "L":
                first_pwds = self.rule_char[value]
            elif key == "D":
                first_pwds = self.rule_number[value]
        except:
            first_pwds = []

        if(len(patterns) > 1):
            last_pwds = self._generate_by_pattern(patterns[1:], p)
   
            res = []
            for first_pwd in first_pwds[:self.limit]:
                for last_pwd in last_pwds[:self.limit]:
                    res.append([first_pwd[0] + last_pwd[0], first_pwd[1] * last_pwd[1]])
            return res
        else:
            return first_pwds

if __name__ == "__main__":
    pcfg = PCFG()
    gen_pwds = pcfg.generate()
    with open(f'./{FILE_NAME}_genpwds.txt', 'w') as f:
        for gen_pwd in gen_pwds[:200000]:
            f.write(f'{gen_pwd[0]} {gen_pwd[1]}\n')
    
    test(FILE_NAME)


