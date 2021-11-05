# Web安全口令猜解之基础分析

## 0x00.实验基础环境

- OS：Windows
- 编程语言：Python
- 第三方库：pyecharts, pickle

## 0x01. 数据预处理

1. 目的：将数据从原始数据中提取出来，存放在txt文件中。

2. 源数据路径: ./raw_data/plaintxt_csdn/www.csdn.net.sql和./raw_data/plaintxt_yahoo/plaintxt_yahoo.txt。（GitHub未上传）

3. 结果存放路径：./data/csdn.txt和./data/yahoo.txt。（github未上传)

## 0x02. 组成模式分析

### 1. 基础代码功能

#### 1.1 init_data()

为两类口令数据集建立统一的读取接口，将口令集读取到列表中

Tips：有些密码中包含又分割符，因此采用了多层拼接模式以期获取完整密码

> Example：`280:robertlevine2000@yahoo.com:ing:ing` 需要按照 `:` 分割后将第二个 `:` 后的内容完全拼接才是完整密码

#### 1.2 components_analysis()

分析口令字典中的元素组成模式，有如下几种:

1. 数字，小写字母，大写字母，其它字符

2. 数字+小写字母，数字+大写字母，数字+其它字符，小写+大写，小写+其它，大写+其它

3. 数字+小写字母+大写字母，数字+小写字母+其它字符，小写+大写+其它

#### 1.3 length_analysis()

分析口令字典中的长度分布规律

#### 1.4 pattern_analysis()

统计令字典中的模式规律，以 N 代表数字，A 代表字母，O 代表其它字符，则一条口令的模式可能是 AAANNNNNO

此外将模式进一步缩减，忽略长度信息，更高层次的查看模式规则：即将 `AAANNNNNO` 模式看为 `ANO` 模式

#### 1.5 topN()

将口令转为模式后，输入到 topN 以期获得最常见的前 N 种结构

#### 1.6 show_pie()

使用 pyecharts 库绘制分析结构的图表，根据标签以及对应的数值，绘制饼图查看其占比

#### 1.7 部署与运行

- 在程序所在目录准备好口令集文件后，依据其分隔符以及密码所在位置对 init_data() 函数进行适当地改动，确保程序正确读入口令集即可

- 最终将会依据该口令集以及口令集的名称输出四类分析文件：`*长度分析.html`，`*组成元素分析.html`，`topn_*构成模式_advance.html`，`topn_*构成模式_base.html`


## 0x03.日期密码格式分析

1. 本部分对应的代码为analysis_task_2.py、task_2_date_pie.py，其中analysis_task_2.py是使用35种日期密码格式分别对csdn、yahoo的密码进行匹配，分别输出在csdn、yahoo密码中各类格式的个数。task_2_date_pie.py能够对35种密码格式用饼状图进行展示。

2. 在具体的使用中，在analysis_task_2.py可以通过修改FILE_NAME来决定输入数据是csdn或者yahoo，task_2_data_pie.py能够将饼状图以html的形式在浏览器中进行查看。


## 0x04.拼音与英文单词分析

1. 基本思路：利用齐夫定律(Zipf's law)，使用根据频率进行排名的语料库，使用动态规划算法，从密码中选取最优的拼音和英文单词组合。

2. 语料库路径：./lib文件夹。该文件夹中包含维基百科语料库(./lib/word_lib.txt)以及常见汉语词组拼音语料库(./lib/pinyin_lib.txt)。

3. 中文英文单词提取：./analysis_task_3.py。通过修改语料库路径lib_path以及数据集路径FILE_NAME进行不同任务。得到提取出的单词/拼音与其出现次数的元组，并按照频数排名。使用方法：
    ```bash
    python ./analysis_task_3.py
    ```

4. 画图：./task_3_pictures.py。根据上一步得到的单词/拼音与其出现次数的元组，得到不同数据集中各个长度单词/拼音中出现频数最高的结果，以便后续PCFG算法使用。得到的图片保存在./results文件夹中。其中：
   
    - csdn_length_pinyin_analysis.html：csdn数据集中长度为1~10分别出现最多的拼音。
    - csdn_length_word_analysis.html：csdn数据集中长度为1~10分别出现最多的单词。
    - yahoo_length_pinyin_analysis.html：yahoo数据集中长度为1~10分别出现最多的拼音。
    - yahoo_length_pinyin_analysis.html：yahoo数据集中长度为1~10分别出现最多的单词。

    使用方法：
    ```bash
    python ./task_3_pictures.py
    ```

## 0x05.生成PCFG模式规则

1. 主要思路：用L代表小写字母，U代表大写字母，D代表数字，S代表特殊符号。将字符串的模式统计出来。例如'password123@!'模式为L8D3S2。

2. 源数据：PCFG算法使用的训练集。（github中未上传）

3. 得到的结果：各种模式及其出现的频率。

4. 结果存放路径：./results/CSDN_rules.pkl和./results/yahoo_rules.pkl。

5. 使用方法：
    ```bash
    python ./analysis_task_4.py
    ```

## 0x06. 合成词库

1. 目的：将csdn和yahoo数据集中得到的单词和拼音及其频数合并，得到新的集合，以便PCFG使用。

2. 源数据：PCFG算法使用的训练集。（github中未上传）

3. 结果存放路径：./results/csdn_lib_pcfg.txt和./results/yahoo_lib_pcfg.txt

4. 使用方法：
    ```bash
    python ./analysis_task_5.py
    ```