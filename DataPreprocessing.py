import os
import io


def main():
    yahoo_dir = './raw_data/plaintxt_yahoo/plaintxt_yahoo.txt'
    with open(yahoo_dir, 'r', encoding='unicode_escape') as f:
        lines = f.readlines()
        header = lines[3070]
        datalines = lines[3072: 3072+453491+1]

        with open('./data/yahoo.txt', 'w', encoding='utf-8') as wfile:
            wfile.writelines(datalines)
        wfile.close()
    f.close()
    
    csdn_dir = 'D:\\MyStudy\\UCAS\\Web_Security\\raw_data\\plaintxt_csdn\\www.csdn.net_utf-8.txt'
    with open(csdn_dir, 'r', encoding='utf-8') as f:
        lines = f.readlines()

        with open('./data/csdn.txt', 'w', encoding='utf-8') as wfile:
            wfile.writelines(lines)
        wfile.close()
    f.close()


if __name__ == "__main__":
    main()