import re
import pickle

FILE_NAME = 'yahoo'
# FILE_NAME = 'csdn'
FILE_PATH = '../data/' + FILE_NAME + ".txt"
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

    # [1]年+月+日、年+月、年、月+日+年、日+月+年
    # [2]小写英文+年+月+日、小写英文+年+月、小写英文+年、小写英文+月+日+年、小写英文+日+月+年
    # [3]大写英文+年+月+日、大写英文+年+月、大写英文+年、大写英文+月+日+年、大写英文+日+月+年
    # [4]其他+年+月+日、其他+年+月、其他+年、其他+月+日+年、其他+日+月+年
    # [5]小写+大写+年+月+日、小写+大写+年+月、小写+大写+年、小写+大写+月+日+年、小写+大写+日+月+年
    # [6]小写+其他+年+月+日、小写+其他+年+月、小写+其他+年、小写+其他+月+日+年、小写+其他+日+月+年
    # [7]大写+其他+年+月+日、大写+其他+年+月、大写+其他+年、大写+其他+月+日+年、大写+其他+日+月+年
    infos_1 = [0] * 5
    infos_2 = [0] * 5
    infos_3 = [0] * 5
    infos_4 = [0] * 5
    infos_5 = [0] * 5
    infos_6 = [0] * 5
    infos_7 = [0] * 5
    result = []

    for i, password in enumerate(passwords):
        if re.match(r'[0-9]+$', password):  # 仅日期
            if len(password) == 8:
                if 1900 <= int(password[0:4]) <= 2021 and 1 <= int(password[4:6]) <= 12 and 1 <= int(password[6:8]) <= 31:
                    infos_1[0] += 1         # 年+月+日 19890524
                if 1900 <= int(password[4:8]) <= 2021 and 1 <= int(password[0:2]) <= 12 and 1 <= int(password[2:4]) <= 31:
                    infos_1[3] += 1         # 月+日+年 05241989
                if 1900 <= int(password[4:8]) <= 2021 and 1 <= int(password[2:4]) <= 12 and 1 <= int(password[0:2]) <= 31:
                    infos_1[4] += 1         # 日+月+年 24051989
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
                    if 1900 <= int(s[0][4:8]) <= 2021 and 1 <= int(s[0][0:2]) <= 12 and 1 <= int(s[0][2:4]) <= 31:
                        infos_2[3] += 1     # 小写英文+月+日+年
                    if 1900 <= int(s[0][4:8]) <= 2021 and 1 <= int(s[0][2:4]) <= 12 and 1 <= int(s[0][0:2]) <= 31:
                        infos_2[4] += 1     # 小写英文+日+月+年
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
                    if 1900 <= int(s[0][4:8]) <= 2021 and 1 <= int(s[0][0:2]) <= 12 and 1 <= int(s[0][2:4]) <= 31:
                        infos_3[3] += 1     # 大写英文+月+日+年
                    if 1900 <= int(s[0][4:8]) <= 2021 and 1 <= int(s[0][2:4]) <= 12 and 1 <= int(s[0][0:2]) <= 31:
                        infos_3[4] += 1     # 大写英文+日+月+年
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
                    if 1900 <= int(s[0][4:8]) <= 2021 and 1 <= int(s[0][0:2]) <= 12 and 1 <= int(s[0][2:4]) <= 31:
                        infos_4[3] += 1     # 其他+月+日+年
                    if 1900 <= int(s[0][4:8]) <= 2021 and 1 <= int(s[0][2:4]) <= 12 and 1 <= int(s[0][0:2]) <= 31:
                        infos_4[4] += 1     # 其他+日+月+年
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
                    if 1900 <= int(s[0][4:8]) <= 2021 and 1 <= int(s[0][0:2]) <= 12 and 1 <= int(s[0][2:4]) <= 31:
                        infos_5[3] += 1     # 小写+大写+月+日+年
                    if 1900 <= int(s[0][4:8]) <= 2021 and 1 <= int(s[0][2:4]) <= 12 and 1 <= int(s[0][0:2]) <= 31:
                        infos_5[4] += 1     # 小写+大写+日+月+年
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
                    if 1900 <= int(s[0][4:8]) <= 2021 and 1 <= int(s[0][0:2]) <= 12 and 1 <= int(s[0][2:4]) <= 31:
                        infos_6[3] += 1     # 小写+其他+月+日+年
                    if 1900 <= int(s[0][4:8]) <= 2021 and 1 <= int(s[0][2:4]) <= 12 and 1 <= int(s[0][0:2]) <= 31:
                        infos_6[4] += 1     # 小写+其他+日+月+年
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
                    if 1900 <= int(s[0][4:8]) <= 2021 and 1 <= int(s[0][0:2]) <= 12 and 1 <= int(s[0][2:4]) <= 31:
                        infos_7[3] += 1     # 大写+其他+月+日+年
                    if 1900 <= int(s[0][4:8]) <= 2021 and 1 <= int(s[0][2:4]) <= 12 and 1 <= int(s[0][0:2]) <= 31:
                        infos_7[4] += 1     # 大写+其他+日+月+年
                elif len(s[0]) == 6:
                    if 1900 <= int(s[0][0:4]) <= 2021 and 1 <= int(s[0][4:6]) <= 12:
                        infos_7[1] += 1     # 大写+其他+年+月
                elif len(s[0]) == 4:
                    if 1900 <= int(s[0][0:4]) <= 2021:
                        infos_7[2] += 1     # 大写+其他+年
    for i in infos_1:
        result.append(i)
    for i in infos_2:
        result.append(i)
    for i in infos_3:
        result.append(i)
    for i in infos_4:
        result.append(i)
    for i in infos_5:
        result.append(i)
    for i in infos_6:
        result.append(i)
    for i in infos_7:
        result.append(i)
    return result

if __name__ == '__main__':
    passwords = init_data()
    # csdn = open(r'./mid/csdn_date_result.pkl', 'wb')
    # yahoo = open(r'./mid/yahoo_date_result.pkl', 'wb')
    # F = open(r'data_csdn.pkl', 'rb')
    # E = open(r'data_yahoo.pkl', 'rb')
    # passwords_csdn = pickle.load(F)
    # passwords_yahoo = pickle.load(E)
    # passwords_csdn = passwords_csdn[0]
    # passwords_yahoo = passwords_yahoo[0]
    print(components_analysis(passwords))
    # pickle.dump(components_analysis(passwords_csdn)[0:2] + components_analysis(passwords_csdn)[3:6], csdn)
    # pickle.dump(components_analysis(passwords_yahoo)[0:2] + components_analysis(passwords_yahoo)[3:6], yahoo)
