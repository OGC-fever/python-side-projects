import geopandas as gp
import pandas as pd
import bs4
import requests
import io
import os
import numpy as np
from bs4 import BeautifulSoup as bs
from zipfile import ZipFile as zf
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.patheffects as pe
import matplotlib.colors
# get data and unpack zipfile
url = 'https://www.water.gov.tw/opendata/qual5.csv'
hardness = pd.read_csv(url)
url_city = 'https://data.gov.tw/dataset/7441'
shp_file, bool_list = [], []
timeout = 3
for i, j in enumerate(os.listdir()):
    bool_list.append('shp' in j)
if True not in bool_list:
    soup_city = bs(io.StringIO(requests.get(url_city, stream=True,
                                            timeout=timeout).content.decode('utf-8')), 'html.parser')
    link_city = soup_city.find('a', text='SHP').get('href')
    with zf(io.BytesIO(requests.get(link_city, stream=True, timeout=timeout).content)) as file_city:
        file_city.extractall()
for i, j in enumerate(os.listdir()):
    if 'shp' in j:
        shp_file.append(j)
# read/filter/select city hardness and map, combine together
map_data = gp.read_file(shp_file[0], encoding='utf-8')
city = np.unique(hardness[hardness.columns[0]].values)
# for i, j in enumerate(city):
#     print(str(i) + '.' + j, end=' ')
#     if (i + 1) % 5 == 0:
#         print()
# city_index = int(input('\nwhich city do you want to query ? '))
'''
0.南投縣 1.嘉義市 2.嘉義縣 3.基隆市 4.宜蘭縣 
5.屏東縣 6.彰化縣 7.新北市 8.新竹市 9.新竹縣 
10.桃園市 11.澎湖縣 12.臺中市 13.臺南市 14.臺東縣 
15.花蓮縣 16.苗栗縣 17.雲林縣 18.高雄市 
'''
city_index = 6
# print('you select : ' + str(city_index) + '.' + city[city_index])
city_data = hardness[hardness[hardness.columns[0]
                              ].str.contains(city[city_index])]
city_data = city_data.sort_values(by=city_data.columns[1])
city_data = city_data.reset_index(drop=1)
city_map = map_data[map_data[map_data.columns[2]
                             ].str.contains(city[city_index])]
city_map = city_map.drop(city_map.columns[[0, 1, 4, 5, 6]], axis=1)
city_map = city_map.sort_values(by=city_map.columns[1])
city_map = city_map.reset_index(drop=1)
plot_data = city_map.join(city_data)
plot_data = plot_data.drop(plot_data.columns[[-2, -3]], axis=1)
# set plot and show
mpl.rcParams['font.sans-serif'] = ['Noto Sans CJK JP', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = "sans-serif"
fig, ax = plt.subplots()
step = 5
level = 300 / step
norm = matplotlib.colors.BoundaryNorm(np.arange(0, 301, level), step)
cmap = plt.get_cmap('RdYlGn_r', step)
path_effects = [pe.withStroke(linewidth=1, foreground='white')]
show = plot_data.plot(column=plot_data[plot_data.columns[-1]],
                      ax=ax, cmap=cmap, edgecolor='black', linewidth=1, norm=norm)
for i in range(len(plot_data)):
    show.annotate(s=plot_data[plot_data.columns[1]][i], xy=(plot_data.centroid.x[i], plot_data.centroid.y[i]),
                  ha='center', va='center', fontsize='large', weight='bold', color='black', path_effects=path_effects)
plt.axis('equal')
ax.axis('off')
ax.set_title(city[city_index] + "自來水硬度", fontsize='x-large')
plt.tight_layout()
# set legend
colors = list(map(cmap, range(step)))
handles = [plt.Rectangle((0, 0), 3, 6, facecolor=c,
                         edgecolor='black', linewidth=0.5) for c in colors]
labels = ["0~60:軟水", "61~120:中等軟水", "121~180:硬水", ">181:超硬水", ">241:你在喝沙?"]
leg = ax.legend(handles, labels, loc=0, prop={'size': 'large'})
leg.set_title(title='硬度:mg/L', prop={'size': 'large'})
plt.show()