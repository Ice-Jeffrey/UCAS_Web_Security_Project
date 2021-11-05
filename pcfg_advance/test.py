
import pickle
from progress.bar import Bar
from utils import load_data

FILE_NAME = 'yahoo'
# FILE_NAME = 'csdn'


def test(file_name):
    _, test_data = load_data(f'./data/data_{file_name}.pkl')
    with open(f'./{file_name}_genpwds.txt', 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    gen_pwds = [line.split(' ')[0].strip() for line in lines]

    total_count = len(test_data)
    match_count = 0
    matched_lst = []

    bar = Bar(max=len(test_data))
    for data in test_data:
        if(data in gen_pwds):
            match_count += 1
            matched_lst.append(data)
        bar.next()
    bar.finish()

    acc = float(match_count) / float(total_count)
    print(acc)
    with open('res.txt', 'a', encoding='utf-8') as f:
        f.write('{}\n'.format(acc))

    matched_str = '\n'.join([str(item) for item in matched_lst])
    with open('info.txt', 'a', encoding='utf-8') as f:
        f.write(matched_str)


def main():
    test(FILE_NAME)

if __name__ == '__main__':
    main()