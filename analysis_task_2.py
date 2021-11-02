import re

# FILE_NAME = 'yahoo'
FILE_NAME = 'csdn'
FILE_PATH = FILE_NAME + ".txt"
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


def components_analysis(passwords):

    # [1]年+月+日、年+月、年
    # [2]小写英文+年+月+日、小写英文+年+月、小写英文+年
    # [3]大写英文+年+月+日、大写英文+年+月、大写英文+年
    # [4]其他+年+月+日、其他+年+月、其他+年
    # [5]小写+大写+年+月+日、小写+大写+年+月、小写+大写+年
    # [6]小写+其他+年+月+日、小写+其他+年+月、小写+其他+年
    # [7]大写+其他+年+月+日、大写+其他+年+月、大写+其他+年
    infos_1 = [0] * 3
    infos_2 = [0] * 3
    infos_3 = [0] * 3
    infos_4 = [0] * 3
    infos_5 = [0] * 3
    infos_6 = [0] * 3
    infos_7 = [0] * 3

    for i, password in enumerate(passwords):
        if re.match(r'[0-9]+$', password):  # 仅日期
            if len(password) == 8:
                if 1900 <= int(password[0:4]) <= 2021 and 1 <= int(password[4:6]) <= 12 and 1 <= int(password[6:8]) <= 31:
                    infos_1[0] += 1         # 年+月+日 19890524
            elif len(password) == 6:
                if 1900 <= int(password[0:4]) <= 2021 and 1 <= int(password[4:6]) <= 12:
                    infos_1[1] += 1         # 年+月 198909
            elif len(password) == 4:
                if 1900 <= int(password[0:4]) <= 2021:
                    infos_1[2] += 1         # 年 1978

        elif(re.match(r'[0-9a-z]+$', password)):
            pattern1 = re.compile(r'[0-9]+')
            s = pattern1.findall(password)
            if len(s) == 1:
                if len(s[0]) == 8:
                    if 1900 <= int(s[0][0:4]) <= 2021 and 1 <= int(s[0][4:6]) <= 12 and 1 <= int(s[0][6:8]) <= 31:
                        infos_2[0] += 1     # 小写英文+年+月+日，如'era19890812'
                elif len(s[0]) == 6:
                    if 1900 <= int(s[0][0:4]) <= 2021 and 1 <= int(s[0][4:6]) <= 12:
                        infos_2[1] += 1     # 小写英文+年+月，如'xs197609'
                elif len(s[0]) == 4:
                    if 1900 <= int(s[0][0:4]) <= 2021:
                        infos_2[2] += 1     # 小写英文+年，如'adsf1976'
        elif(re.match(r'[0-9A-Z]+$', password)):
            pattern1 = re.compile(r'[0-9]+')
            s = pattern1.findall(password)
            if len(s) == 1:
                if len(s[0]) == 8:
                    if 1900 <= int(s[0][0:4]) <= 2021 and 1 <= int(s[0][4:6]) <= 12 and 1 <= int(s[0][6:8]) <= 31:
                        infos_3[0] += 1     # 大写英文+年+月+日
                elif len(s[0]) == 6:
                    if 1900 <= int(s[0][0:4]) <= 2021 and 1 <= int(s[0][4:6]) <= 12:
                        infos_3[1] += 1     # 大写英文+年+月
                elif len(s[0]) == 4:
                    if 1900 <= int(s[0][0:4]) <= 2021:
                        infos_3[2] += 1     # 大写英文+年
        elif(re.match(r'[^a-zA-Z]+$', password)):
            pattern1 = re.compile(r'[0-9]+')
            s = pattern1.findall(password)
            if len(s) == 1:
                if len(s[0]) == 8:
                    if 1900 <= int(s[0][0:4]) <= 2021 and 1 <= int(s[0][4:6]) <= 12 and 1 <= int(s[0][6:8]) <= 31:
                        infos_4[0] += 1     # 其他+年+月+日
                elif len(s[0]) == 6:
                    if 1900 <= int(s[0][0:4]) <= 2021 and 1 <= int(s[0][4:6]) <= 12:
                        infos_4[1] += 1     # 其他+年+月
                elif len(s[0]) == 4:
                    if 1900 <= int(s[0][0:4]) <= 2021:
                        infos_4[2] += 1     # 其他+年
        elif(re.match(r'[0-9a-zA-Z]+$', password)):
            pattern1 = re.compile(r'[0-9]+')
            s = pattern1.findall(password)
            if len(s) == 1:
                if len(s[0]) == 8:
                    if 1900 <= int(s[0][0:4]) <= 2021 and 1 <= int(s[0][4:6]) <= 12 and 1 <= int(s[0][6:8]) <= 31:
                        infos_5[0] += 1     # 小写+大写+年+月+日
                elif len(s[0]) == 6:
                    if 1900 <= int(s[0][0:4]) <= 2021 and 1 <= int(s[0][4:6]) <= 12:
                        infos_5[1] += 1     # 小写+大写+年+月
                elif len(s[0]) == 4:
                    if 1900 <= int(s[0][0:4]) <= 2021:
                        infos_5[2] += 1     # 小写+大写+年
        elif(re.match(r'[^A-Z]+$', password)):
            pattern1 = re.compile(r'[0-9]+')
            s = pattern1.findall(password)
            if len(s) == 1:
                if len(s[0]) == 8:
                    if 1900 <= int(s[0][0:4]) <= 2021 and 1 <= int(s[0][4:6]) <= 12 and 1 <= int(s[0][6:8]) <= 31:
                        infos_6[0] += 1     # 小写+其他+年+月+日
                elif len(s[0]) == 6:
                    if 1900 <= int(s[0][0:4]) <= 2021 and 1 <= int(s[0][4:6]) <= 12:
                        infos_6[1] += 1     # 小写+其他+年+月
                elif len(s[0]) == 4:
                    if 1900 <= int(s[0][0:4]) <= 2021:
                        infos_6[2] += 1     # 小写+其他+年
        elif(re.match(r'[^a-z]+$', password)):
            pattern1 = re.compile(r'[0-9]+')
            s = pattern1.findall(password)
            if len(s) == 1:
                if len(s[0]) == 8:
                    if 1900 <= int(s[0][0:4]) <= 2021 and 1 <= int(s[0][4:6]) <= 12 and 1 <= int(s[0][6:8]) <= 31:
                        infos_7[0] += 1     # 大写+其他+年+月+日
                elif len(s[0]) == 6:
                    if 1900 <= int(s[0][0:4]) <= 2021 and 1 <= int(s[0][4:6]) <= 12:
                        infos_7[1] += 1     # 大写+其他+年+月
                elif len(s[0]) == 4:
                    if 1900 <= int(s[0][0:4]) <= 2021:
                        infos_7[2] += 1     # 大写+其他+年
    for i in infos_1:
        print(i)
    for i in infos_2:
        print(i)
    for i in infos_3:
        print(i)
    for i in infos_4:
        print(i)
    for i in infos_5:
        print(i)
    for i in infos_6:
        print(i)
    for i in infos_7:
        print(i)

if __name__ == '__main__':
    passwords = init_data()
    components_analysis(passwords)
