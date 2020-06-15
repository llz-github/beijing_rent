1. zufang.csv是链家网爬取下的北京市租房数据，直接打开可能会造成乱码，可以用__文本文件__打开，点击文件--另存为--选择编码格式为ANSI即可。
2. house_data_crawler.py是爬取链家网北京市租房信息的爬虫文件。
3. info.py 是供house_data_crawler.py 调用的文件，配置了要爬取的地区代码。
4. random_ip_and_header.py 是一个独立的随机获取 ip 和 header 的文件,这里为 house_data_crawler.py 提供随机的 ip 和 header
5.  zufang.json 本文件是爬取下的数据 josn 版。
