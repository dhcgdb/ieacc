from os import name
from typing import Any
import matplotlib

matplotlib.use('cairo')
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from numpy.core.fromnumeric import mean

STEP = 500
PACKET = 1024
VINDEX = 17

nameset = ['10:0', '9:1', '8:2', '7:3', '6:4']
suffixset = ['100', '91', '82', '73', '64']
itemset = ['ddpg', 'dqn']
count = len(suffixset)
y1 = [[] for _ in range(count)]
y2 = [[] for _ in range(count)]

index = 0
stepx = 0
for suffix in suffixset:
    file1 = '/root/ndn/proj-sep/log/reexp/ddpg-c1-' + str(suffix) + '-0.log'
    file2 = '/root/ndn/proj-sep/log/reexp/dqn-c1-' + str(suffix) + '-0.log'
    lines1 = open(file1, 'r').readlines()
    lines2 = open(file2, 'r').readlines()
    for line in lines1:
        value = line.replace(' ', '').split(',')
        if (len(value) >= 3 and value[2] == 'data'):
            if stepx % STEP == 0:
                y1[index].append(float(value[VINDEX]) * 1000)
            stepx += 1
    for line in lines2:
        value = line.replace(' ', '').split(',')
        if (len(value) >= 3 and value[2] == 'data'):
            if stepx % STEP == 0:
                y2[index].append(float(value[VINDEX]) * 1000)
            stepx += 1
    index += 1

for i in range(len(y1)):
    xf = open("./ddpg-" + suffixset[i] + ".txt", "w")
    xx = y1[i]
    for j in range(len(xx)):
        xf.write(str(xx[j]) + '\n')
    xf.close()
for i in range(len(y2)):
    xf = open("./dqn-" + suffixset[i] + ".txt", "w")
    xx = y2[i]
    for j in range(len(xx)):
        xf.write(str(xx[j]) + '\n')
    xf.close()


ys = []
xs = []
hs = []
for i in range(count):
    ys += (y1[i] + y2[i])
    xs += ([nameset[i]] * (len(y1[i]) + len(y2[i])))
    hs += (['IEACC'] * len(y1[i]) + ['DRL-CCP'] * len(y2[i]))

from pandas.core.frame import DataFrame

data = {"Algorithm": xs, "Delay (ms)": ys}  #将列表a，b转换成字典
data = DataFrame(data)  #将字典转换成为数据框

plt.figure(figsize=(8, 5))
fig = sns.boxplot(
    x="Algorithm",
    y="Delay (ms)",
    data=data,
    hue=hs,
    palette=['red', 'blue'],
    #saturation=0.5,
    width=0.4,
    linewidth=1.0,
    showfliers=True,
    fliersize=2.0,
    medianprops={
        'linestyle': '-',
        'color': 'black'
    },
    whiskerprops={'linestyle': '-.'},
    showmeans=False,
    meanprops={
        'marker': 'D',
        'color': 'blue'
    })
fig.set_xlabel("Ratio", fontsize=16)
fig.set_ylabel("Delay (ms)", fontsize=16)
fig.legend(loc='center left', fontsize=16)
fig.tick_params(labelsize=16)
#plt.ylim(bottom=40)
#plt.xlim((50,110))
plt.grid(axis="y", linestyle='-.')
plt.savefig('./82rtt2-t.pdf')
