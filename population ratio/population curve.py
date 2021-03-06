'''
data source:https://data.gov.tw/dataset/33604
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

csv = "https://quality.data.gov.tw/dq_download_csv.php?nid=33604&md5_url=7fe22230d102a94437d693849e3cd23b"
data = pd.read_csv(csv).iloc[:-2]
new_data = pd.DataFrame(data[data.columns[0:2].append(data.columns[3:])])
plot_data = new_data[new_data.columns[2:]]

ratio = []
for i, _ in enumerate(plot_data.index):
    if i % 2 == 1:
        ratio.append([plot_data.iloc[i-1].values/plot_data.iloc[i].values])

ratio=np.array(ratio).reshape(-1)
for i,_ in enumerate(ratio):
    if ratio[i] == ((np.inf or -np.inf) or np.nan):
        ratio[i] = 0
ratio = np.array(ratio).reshape(-1, len(plot_data.columns))

add_array = []
for i in range(2):
    add_array.append(list(range(i, int(len(plot_data.index)/2), 2)))

total_ratio = [[], []]

for i in range(2):
    total_ratio[i] = plot_data.iloc[add_array[i]].sum()
total_ratio = total_ratio[0]/total_ratio[1]

def show_town():
    for i in range(int(len(new_data[new_data.columns[0]])/2)):
        town.append((new_data[new_data.columns[0]].values[i*2]))
#     for i in range(len(town)):
#         if (i+1) % 7 != 0:
#             print(str(i) + " " + town[i], end=' ')
#         else:
#             print(str(i) + " " + town[i])

plt.figure()

def set_plt():
    plt.rcParams['font.sans-serif'] = ['Noto Sans CJK JP', 'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.family'] = "sans-serif"
    plt.rcParams.update({'font.size': 14})

set_plt()
town = []
show_town()
# select_town=int(input("\nwhich one to show?\n"))-1
'''
0 彰化市 1 員林市 2 鹿港鎮 3 和美鎮 4 北斗鎮 5 溪湖鎮 6 田中鎮
7 二林鎮 8 線西鄉 9 伸港鄉 10 福興鄉 11 秀水鄉 12 花壇鄉 13 芬園鄉
14 大村鄉 15 埔鹽鄉 16 埔心鄉 17 永靖鄉 18 社頭鄉 19 二水鄉 20 田尾鄉
21 埤頭鄉 22 芳苑鄉 23 大城鄉 24 竹塘鄉 25 溪州鄉
'''
select_town = 8
# towns=[0,1,5]
plt.title("彰化縣男女比率-年齡分佈", fontsize='x-large')
plt.plot(total_ratio, 'C0-.', label='彰化縣')
plt.plot(ratio[select_town], 'C1-.', label=town[select_town])
# plt.subplots(1,3)
plt.axhline(y=1, color='gray')
plt.legend(loc=0)
plt.grid()
plt.xticks(range(0, 101, 10))
plt.xlabel("age")
plt.ylabel("male/female ratio")
plt.show()