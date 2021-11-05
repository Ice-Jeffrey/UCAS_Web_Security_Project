# Web安全口令猜解

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

4. 画图：./task_3_pictures.py。根据上一步得到的单词/拼音与其出现次数的元组，得到不同数据集中各个长度单词/拼音中出现频数最高的结果，以便后续PCFG算法使用。得到的图片保存在./analysis/results文件夹中。其中：
   
    - csdn_length_pinyin_analysis.html：csdn数据集中长度为1~10分别出现最多的拼音。
    - csdn_length_word_analysis.html：csdn数据集中长度为1~10分别出现最多的单词。
    - yahoo_length_pinyin_analysis.html：yahoo数据集中长度为1~10分别出现最多的拼音。
    - yahoo_length_pinyin_analysis.html：yahoo数据集中长度为1~10分别出现最多的单词。

    使用方法：
    ```bash
    cd analysis
    python ./task_3_pictures.py
    ```

## 0x05.生成PCFG模式规则

1. 主要思路：用L代表小写字母，U代表大写字母，D代表数字，S代表特殊符号。将字符串的模式统计出来。例如'password123@!'模式为L8D3S2。

2. 源数据：PCFG算法使用的训练集。（github中未上传）

3. 得到的结果：各种模式及其出现的频率。

4. 结果存放路径：./analysis/results/CSDN_rules.pkl和./analysis/results/yahoo_rules.pkl。

5. 使用方法：
    ```bash
    cd analysis
    python ./analysis_task_4.py
    ```

## 0x06. 合成词库

1. 目的：将csdn和yahoo数据集中得到的单词和拼音及其频数合并，得到新的集合，以便PCFG使用。

2. 源数据：PCFG算法使用的训练集。（github中未上传）

3. 结果存放路径：./analysis/results/csdn_lib_pcfg.txt和./analysis/results/yahoo_lib_pcfg.txt

4. 使用方法：
    ```bash
    cd analysis
    python ./analysis_task_5.py
    ```

## 0x07. PCFG算法

### Advanced PCFG

对大量口令进行模式分析，规则提取后生成高质量口令字典

### 目录结构与说明

`./data/*`：对 csdn 与 yahoo 口令按照分析结果进行筛选后，分解为训练集与测试集后的结果

`./csdn/*`：基于 csdn 数据集生成的有效规则序列与有效模式序列（筛选后的结果）

`./yahoo/*`：基于 yahoo 数据集生成的有效规则序列与有效模式序列（筛选后的结果）

> char_rule：基于密码中最长相邻字符串统计的规则
>
> char_lib：基于常见英文或拼音并使用**齐夫定律**提取的字符串统计的规则
>
> number_rule：基于密码中最长相邻数字统计的规则
>
> pattern：基于密码中的模式统计出的规则

`./*_genpwds.txt`：最终生成的口令字典

`./split_data.py`：实现对原始口令集合的筛选与数据集切分

`./generate_rules.py`：针对输入的数据集生成规则信息

`./pcfg.advance.py`：实现规则增强的 PCFG 算法

`./test.py`：根据生成的口令字典在测试集中进行撞库测试

`./utils.py`：通用的工具类函数

### PCFG 算法

#### init

算法初始化模块，根据数据集名称导入规则文件与模式文件，并：

1、将规则文件映射为字典，其 key 值为规则的长度，其 value 值为列表（存储长度一致的规则内容）

> 其中针对字符串规则有一类是根据最长字符串匹配得到的统计规则，还有一类是基于常见英文或拼音并使用**齐夫定律**提取的字符串统计的规则，我们后续针对这两类规则进行了对比实验

2、将模式分为元组的形式方便后续处理：`Example: [('L', 3), ('D', 3), ('L', 1), p]`

#### generate

根据常见的模式与规则进行算法的生成，特殊的是针对较深的递归考虑到频率的叠加将会造成可能性的极度降低，因此较深的（>=3）的模式将被忽略，然后又考虑到算力与算法的效率，针对数据集的数目进行了递归基数的限制（`self.limit`），如果你将使用本算法进行测试，可以执行尝试调节该参数以期达到更好的效果

#### main

1、需要配置好 init 函数的参数，绑定好目标规则文件，随后即可完成类的初始化（规则文件与模式文件的加载）

2、文件加载后即可执行 generate() 函数，他将以列表的形式返回所有生成的口令

3、选择前 N 个将生成的口令写入到本地文件

### 执行

#### split_data.py

首先需要运行 `split_data.py` 其输入为原始的口令数据文件

1、需要在 `init_data()` 模块定义文件的加载规则

2、需要在 `_filter_data()` 模块自定义其过滤规则

3、需要在 `_split_data()` 模块自定义训练集测试集比例，将数据集分割

最后分割的数据集将持久化保存到 `./data/*`

#### generate_rule.py

根据配置信息中的 `FILE_NAME` 变量将自动化的加载分割后的数据集，使用训练集运行得到最初的规则文件保存到 `./{FILE_NAME}/*` 中

#### pcfg.advance.py

1、需要配置好 init 函数的参数，绑定好目标规则文件，随后即可完成类的初始化（规则文件与模式文件的加载）

2、文件加载后即可执行 generate() 函数，他将以列表的形式返回所有生成的口令

3、选择前 N 个将生成的口令写入到本地文件 `./*_genpwds.txt`

