#!/usr/bin/env python 
# coding:utf-8
from collections import Counter
import os
import pickle
import re
from pyecharts import options as opts
from pyecharts.charts import Page, Pie

def show_pie(title, labels, values):
    pie = (
        Pie()
            .add("", [list(z) for z in zip(labels, values)], radius=["30%","50%"], center=["40%","60%"])
            .set_global_opts(title_opts=opts.TitleOpts(title=title),
                            legend_opts=opts.LegendOpts(
                                orient="vertical", pos_top="5%", pos_right="2%"  # 左面比例尺
                                ),
                            )
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
        )
    pie.render(title + '.html')


FILE_NAME = 'yahoo'
#FILE_NAME = 'csdn'
FILE_PATH = "../data/" + FILE_NAME + ".txt"  # 453491
TOTAL_COUNT = None

def main():
    components = ['年月日', '年月', '年', '月日年', '日月年',  '小写英文+年月日', '小写英文+年月', '小写英文+年',
                  '小写英文+月日年', '小写英文+日月年', '大写英文+年月日', '大写英文+年月', '大写英文+年', '大写英文+月日年', '大写英文+日+月+年', '其他+年月日', '其他+年月',
                  '其他+年', '其他+月日年', '其他+日月年', '小写+大写+年月日', '小写+大写+年月', '小写+大写+年', '小写+大写+月日年', '小写+大写+日月年', '小写+其他+年月日',
                  '小写+其他+年月', '小写+其他+年', '小写+其他+月日年', '小写+其他+日月年', '大写+其他+年月日', '大写+其他+年月', '大写+其他+年', '大写+其他+月日年', '大写+其他+日月年']
    values = [162, 66, 125, 902, 875, 43, 46, 10988, 256, 221, 3, 1, 189, 17, 16, 1, 0, 1, 0, 0, 2, 7, 1073, 20, 20, 0, 1, 291, 4, 10, 1, 0, 14, 2, 1]
    #values = [397206, 552, 138, 3754, 5660, 97641, 9724, 94997, 1095, 1725, 6734, 752, 4726, 65, 165, 1412, 78, 78, 17, 22, 2872, 240, 4349, 30, 40, 4314, 372, 8908, 44, 52, 450, 32, 550, 3, 2]
    show_pie(FILE_NAME + '日期密码格式统计', components, values)

if __name__ == '__main__':
    main()
