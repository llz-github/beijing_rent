#!/usr/bin/env python
# coding: utf-8

# # 目录
# ## 1.读取数据并与处理数据
# #### 1.1读取数据
# #### 1.2异常数据预处理
# #### 1.3数据预处理
# #### 1.4数据保存
# ## 2.数据分析
# ### 提出问题
# #### 2.1北京出租房区域分布分析
# #### 2.2出房屋的主要类型分析
# #### 2.3各区域平均租金分析
# #### 2.4出租屋面积分布
# #### 2.5按需分析划分宜居地
# #### 2.6在地图上显示宜居地所处北京市的具体位置（热力图）
# ## 3.友情链接（本项目技能学习处）

# # 1.读取数据*__并预处理__*数据

# # 1.1读取数据

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


data_s = pd.read_csv("F:/MongoDB/data/zufang.csv",sep=",")
print("北京租房信息前五行:\n")
data_s.head()


# In[3]:


print("北京租房信息规格:",data_s.shape)
print("北京租房基本信息:",data_s.info())


# # 1.2异常数据预处理

# In[4]:


# 删除重复行
print(data_s.shape)
data = data_s.drop_duplicates()
print(data.shape)


# In[5]:


# 删除包含空值的行  暂时不删除()
# print(data.shape)
# data = data.dropna()
# print(data.shape)


# In[6]:


#1._id和m_url列没有用了,可以删掉
data = data.drop(columns=["_id","m_url"])
data.head()


# In[7]:


#2.查看bathroom可能的异常数据
data.bathroom_num.unique()    #查看bathroom在数据中存在的数量


# In[8]:


data[data['bathroom_num'].isin(['8','9'])]    #大胡同 有八个bathroom也正常,没有异常数据


# In[9]:


#3.查看bedroom可能的异常数据
data.bedroom_num.unique()    #查看bedroom在数据中存在的数量


# In[10]:


data[data['bedroom_num'].isin(['14','15'])] #公寓,房间多也正常


# In[11]:


#4.查看bizcircle_name能的异常数据
print("bizcircle:\n",data.bizcircle_name.unique())                   #没问题
print("city:\n",data.city.unique())                                  #没问题
print("dist:\n",data.dist.unique())                                  #没问题
# print("distance:\n",data.distance.unique())                        #没问题
print("frame_orientation:\n",data.frame_orientation.unique())        #没问题
print("hall_num:\n",data.hall_num.unique())                          #没问题
# print("house_tag:\n",data.house_tag.unique())                      #没问题
print("latitude:\n",data.latitude.unique())                          #没问题
print("layout:\n",data.layout.unique())                              #没问题
print("longitude:\n",data.longitude.unique())                        #没问题


# In[12]:


#房屋面积
np.sort(data.rent_area.unique(),axis=0)

# print("rent_area:\n",data.rent_area.unique().min())


# In[13]:


data[data['rent_area'].isin(['5','1300','8426','84057','1200'])]    #可能也正常


# In[14]:


# 45009 45182 数据异常,删除
data = data.drop([45009,45182])


# In[15]:


print("rent_price_listing:\n",data.rent_price_listing.unique())      #没问题
print("rent_price_unit:\n",data.rent_price_unit.unique())            #没问题
print("resblock_name:\n",data.resblock_name.unique())                #没问题
print("type:\n",data.type.unique())                                  #没问题


# # 1.3数据预处理

# In[16]:


# 数据类型转换
for col in ['bathroom_num', 'bedroom_num', 'hall_num', 'rent_price_listing']:
    data[col] = data[col].astype(int)


# In[17]:


# 'distance', 'latitude', 'longitude'因为有NaN，需另外处理
def dw_None_latlon(data):
    if data is None or data == '':
        return np.nan
    else:
        return float(data)            


# In[18]:


data['distance'] = data['distance'].apply(dw_None_latlon)
data['latitude'] = data['latitude'].apply(dw_None_latlon)
data['longitude'] = data['longitude'].apply(dw_None_latlon)


# In[19]:


print("北京租房基本信息:",data.info())


# #### 1.4数据保存

# In[21]:


data.to_csv("F:/MongoDB/data/zufang_clear.csv",sep=',',index=False)


# # 2.数据分析

# ## 提出问题
#     1.北京出租房区域分布分析
#     2.出房屋的主要类型分析
#     3.各区域平均租金分析
#     4.出租屋面积分布
#     5.按需分析划分宜居地
#     6.在地图上显示宜居地所处北京市的具体位置（热力图）

# ### 2.1.1 北京出租房区域分布

# In[21]:


import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl

# 设置显示中文字体
mpl.rcParams['font.sans-serif'] = ['SimHei'] 
# 设置正常显示符号
mpl.rcParams['axes.unicode_minus'] = False


# In[22]:


# 区域数据
house_count = data.groupby(['dist']).count()['city']
house_count


# In[23]:


# 数据排序
house_count = house_count.sort_values(ascending=False)


# In[24]:


# 作图
house_count.plot(kind='bar',figsize=(18,8),color='red')
plt.xlabel('区域')                       ## 添加横轴标签
plt.ylabel('出租房数量')                 ## 添加y轴名称
plt.title('北京市出租房数量柱状图')
plt.show()


# 北京市朝阳区出租房数量巨大，其次为海淀、丰台等地区，密云、怀柔和平谷等地几乎没有出租房

# ### 2.2 常见出租房户型

# In[25]:


#户型数量统计
house_type_count = data.groupby(by=['layout']).count()['city']
#排序
house_type_count.sort_values()


# In[26]:


#数据筛选
house_type_df = pd.DataFrame(data={"数量":house_type_count})
house_type_df = house_type_df.sort_values(by=["数量"],ascending=False)
house_type_df


# In[27]:


#去数量大于100的作为常见户型
house_type_df = house_type_df.query("数量>100")
#作图
house_type_df.plot(kind='bar',figsize=(18,8))
plt.xlabel('房屋类型')                       ## 添加横轴标签
plt.ylabel('出租房数量')                 ## 添加y轴名称
plt.title('北京出租房常见户型柱状图')
plt.show()


# 北京市 出租房最常见的户型为：两室一厅一卫、一室一厅一卫、三室一厅一卫、一室一卫等。

# ### 2.3 各区域出租房平均租金分析

# In[28]:


# 新建df对象
df_all = pd.DataFrame({"区域":data["dist"].unique(),"房屋总金额":[0]*len(data["dist"].unique()),"房屋总面积":[0]*len(data["dist"].unique())})
df_all


# In[29]:


sum_price = data['rent_price_listing'].groupby(data['dist']).sum()
sum_area = data['rent_area'].groupby(data['dist']).sum()


# In[30]:


df_all['区域']=sum_area.index
df_all['房屋总面积']=sum_area.values
df_all['房屋总金额']=sum_price.values


# In[31]:


df_all['每平米租金']= round(df_all['房屋总金额'] / df_all['房屋总面积'],2)
df_all


# In[32]:


# 这里的注意不能用house_count,上文中已排序,区域列不符
df_all['数量']=data.groupby(['dist']).count()['city'].values
df_all


# In[35]:


# 绘图
import matplotlib.ticker as mtick
num = df_all['数量']
price = df_all['每平米租金']
l = [i for i in range(len(df_all['数量']))]
lx = df_all["区域"]
#创建画布
fig = plt.figure(figsize=(25,10),dpi=100)
# 获取子图对象
ax1 = fig.add_subplot(111)
ax1.plot(l,price,"or-",label="每平米租金价格")
ax1.set_ylim([0,200])
ax1.set_ylabel('价格')
plt.legend(loc="upper left")

#绘制柱状图
ax2 = ax1.twinx()
plt.bar(l,num,alpha=0.5,color="g",label="数量")
ax2.set_label('数量')
ax2.set_ylim([0,18000])
#显示图例说明
plt.legend(loc="upper right")

plt.title('北京出租房每平米价格分布及房屋数量分布')
# 设置x轴
plt.xticks(l,lx)
plt.show()


# 可以看出，大兴、通州、顺义平均房价相较合适,且选择较多

# ### 2.4 出租屋面积分布

# In[36]:


data['rent_area'].max()


# In[37]:


data['rent_area'].min()


# In[38]:


area_divide = [1,30,60,90,120,150,180,210,1300]
area_cut = pd.cut(data['rent_area'],area_divide)


# In[39]:


ret = area_cut.value_counts().sort_index()
ret


# In[45]:


labels = ['30平米以下','30-60平米','60-90平米','90-120平米','120-150平米','150-180平米','180-210平米','210以上']
plt.figure(figsize=(40,10),dpi=100)
plt.pie(x=ret.values,labels=labels,autopct="%.2f%%")

plt.legend(loc='upper right')
plt.title('北京市出租房主要面积区间占比分布')
plt.show()


# 北京市 出租房面积大多在30 -90 平米这个区间

# ### 2.5  按需分析

# 我们来模拟租房需求进行数据分析：以本人为例，结合个人情况，对户型，以及各种需求进行分析，以追求物美价廉的房子
# 
# 关注集中供暖，民水民电，最好是近地铁，如果价格不合适，稍远一点儿也无所谓
# 本人一人，重点关注一室的房子
# 
# 位置：通州区，大兴区，顺义区。
# 
# 户型：1室1厅1卫、1室0厅1卫、1室0厅0卫、1室1厅0卫。
# 
# 房屋信息：民水民电，集中供暖，近地铁

# In[46]:


# 通州，顺义 大兴的房子
data_me = data[data['dist'].isin(['通州','大兴','顺义'])]
data_me.shape


# In[47]:


data_me = data_me[data_me['bedroom_num'].isin(['1'])]
data_me.shape


# In[48]:


# 去house_tag空值
data_me = data_me.dropna(subset=['house_tag'])
data_me.shape

data_me = data_me[data_me['house_tag'].str.contains('民水民电','集中供暖')]
data_me.shape


# In[49]:


#数量还可以，可继续筛选
data_me = data_me[data_me['house_tag'].str.contains('近地铁')]
data_me.shape


# In[50]:


data_me = data_me[data_me['house_tag'].str.contains('精装修')]
data_me.shape


# In[57]:


# data_me
# df_all2


# In[52]:


# 数据配置
df_all2 = pd.DataFrame({"区域":data_me["bizcircle_name"].unique(),"房屋总金额":[0]*len(data_me["bizcircle_name"].unique()),"房屋总面积":[0]*len(data_me["bizcircle_name"].unique())})
sum_price2 = data_me['rent_price_listing'].groupby(data_me['bizcircle_name']).sum()
sum_area2 = data_me['rent_area'].groupby(data_me['bizcircle_name']).sum()
df_all2['区域']=sum_area2.index
df_all2['房屋总面积']=sum_area2.values
df_all2['房屋总金额']=sum_price2.values
df_all2['每平米租金']= round(df_all2['房屋总金额'] / df_all2['房屋总面积'],2)
df_all2['数量']=data_me.groupby(['bizcircle_name']).count()['city'].values
df_all2


# In[59]:


# 绘图
import matplotlib.ticker as mtick
num = df_all2['数量']
price = df_all2['每平米租金']
l = [i for i in range(len(df_all2['数量']))]
lx = df_all2["区域"]
#创建画布
fig = plt.figure(figsize=(25,10),dpi=100)
# 获取子图对象
ax1 = fig.add_subplot(111)
ax1.plot(l,price,"or-",label="每平米租金价格")
ax1.set_ylim([0,200])
ax1.set_ylabel('价格')
plt.legend(loc="upper left")

#绘制柱状图
ax2 = ax1.twinx()
plt.bar(l,num,alpha=0.5,color="g",label="数量")
ax2.set_label('数量')
ax2.set_ylim([0,80])
#显示图例说明
plt.legend(loc="upper right")
# 设置x轴
plt.xticks(l,lx)
plt.title('北京市本人宜居地分布图')
plt.show()


# 结合本图来看，果园、通州北苑比较符合个人预期的居住地点，每平米的租金相对便宜且可选择对比的房屋数量偏多。
# 
# （如若可选择区域较少，可退至上一步，取消近地铁或精装修选项，重新绘制此图）。

# In[54]:


# 热力图数据准备
data_me = data_me.dropna()
data_me["aver_price"]=data_me['rent_price_listing'] / data_me['rent_area']


# In[55]:


# 绘制热力图
import numpy as np
import pandas as pd
import seaborn as sns
import folium
import webbrowser
from folium.plugins import HeatMap



nums = len(data_me['longitude'])

lat = np.array(data_me['latitude'].values)                        # 获取维度之维度值
lon = np.array(data_me['longitude'].values)                        # 获取经度值
pop = np.array(data_me["aver_price"].values,dtype=float)    # 获取人口数，转化为numpy浮点型

data1 = [[lat[i],lon[i],pop[i]] for i in range(nums)]    #将数据制作成[lats,lons,weights]的形式

map_osm = folium.Map(location=[39.9, 116.3],zoom_start=15)    #绘制Map，开始缩放程度是5倍
HeatMap(data1).add_to(map_osm)  # 将热力图添加到前面建立的map里

file_path = r"F:\MongoDB\data\宜居地.html"
map_osm.save(file_path)     # 保存为html文件

webbrowser.open(file_path)  # 默认浏览器打开


# 以热力图的方式画出宜居地所处北京市的位置，并保存至附件宜居地.html中.
# 
# 所处北京市的位置颜色越深代表每平米价格越贵。

# ## 3.友情链接

# 注：
# windows 下安装配置mongodb 和机器可视化工具adminMongo
# 
# https://llzgithub.github.io/2020/06/11/windows%20%E4%B8%8B%E5%AE%89%E8%A3%85mongodb%20%E6%9C%BA%E5%99%A8%E5%8F%AF%E8%A7%86%E5%8C%96%E5%B7%A5%E5%85%B7adminMongo/
# 
# 爬虫ip代理及angents头设置,防止网站禁止爬虫爬取
# 
# https://llz-github.github.io/2020/06/13/python%E7%88%AC%E8%99%AB%E8%AE%BE%E7%BD%AE%E9%9A%8F%E6%9C%BAip%E5%92%8CUser-Agent/
# 
# 热力图          https://www.cnblogs.com/traditional/p/12386907.html

# In[ ]:





# In[ ]:




