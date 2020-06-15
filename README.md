# 本项目为北京市租房信息数据分析
> 采用Mongo 作为数据库进行信息存储。
> 爬取链家网的数据进行分析
## 咱们从源数据文件加开始
![image-20200615221556639](https://cdn.jsdelivr.net/gh/llz-github/image/img1/20200615222650.png)
1. zufang.csv是链家网爬取下的北京市租房数据，直接打开可能会造成乱码，可以用__文本文件__打开，点击文件--另存为--选择编码格式为ANSI即可。
2. house_data_crawler.py是爬取链家网北京市租房信息的爬虫文件。
3. info.py 是供house_data_crawler.py 调用的文件，配置了要爬取的地区代码。
4. random_ip_and_header.py 是一个独立的随机获取 ip 和 header 的文件,这里为 house_data_crawler.py 提供随机的 ip 和 header
5. zufang.json 本文件是爬取下的数据 josn 版。
## 然后是过程数据
![image-20200615223918249](https://cdn.jsdelivr.net/gh/llz-github/image/img1/20200615224033.png)
> zufang_clear.csv是原始数据经过数据预处理后的数据，直接打开可能会造成乱码，可以用__文本文件__打开，点击文件--另存为--选择编码格式为ANSI即可。
## 各阶段运行结果图
![image-20200615225007924](https://cdn.jsdelivr.net/gh/llz-github/image/img1/20200615225118.png)
1. 数据分析图中是根据一些问题，将数据绘制的柱状图、饼图等
2. 数据预处图是数据新型预处理是各类异常数据等的截图
3. 宜居图是根据本人租房需求，绘制的热力图。
## 程序集模型文件
![image-20200615224924001](https://cdn.jsdelivr.net/gh/llz-github/image/img1/20200615224924.png)
> 数据挖掘--北京租房信息分析.py 是采用链家网的数据进行数据预处理，数据分析的python文件,数据挖掘--北京租房信息分析.html可直接查看，数据挖掘--北京租房信息分析.zip是文档保存的md格式。
