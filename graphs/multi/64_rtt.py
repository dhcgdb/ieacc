from os import name
from typing import Any
import matplotlib

matplotlib.use('cairo')
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from numpy.core.fromnumeric import mean

STEP = 250
PACKET = 1024
VINDEX = 17

nameset = ['IEACC', 'ICP', 'ECP', 'DRL-CCP']
suffixset = ['ddpg', 'aimd', 'ecp', 'dqn']
#suffixset = ['64', '73', '82', '91','100']
count = len(suffixset)
y = [[] for _ in range(count)]

index = 0
stepx = 0
for suffix in suffixset:
    file1 = '/root/ndn/proj-sep/log/multiport/' + suffix + '-c1-drop-82.log'
    lines = open(file1, 'r').readlines()
    for line in lines:
        value = line.replace(' ', '').split(',')
        if (len(value) >= 3 and value[2] == 'data'):
            if stepx % STEP == 0:
                y[index].append(float(value[VINDEX]) * 1000)
            stepx += 1
    index += 1

for i in range(len(y)):
    xf = open("./net-" + suffixset[i] + ".txt", "w")
    xx = y[i]
    for j in range(len(xx)):
        xf.write(str(xx[j]) + '\n')
    xf.close()


ys = y[0]
xs = [nameset[0]] * len(y[0])
for i in range(count - 1):
    ys += y[i + 1]
    xs += [nameset[i + 1]] * len(y[i + 1])
print(len(ys), len(xs))

from pandas.core.frame import DataFrame

data = {"Algorithm": xs, "Delay (ms)": ys}  #将列表a，b转换成字典
data = DataFrame(data)  #将字典转换成为数据框

plt.figure(figsize=(5, 5))
fig = sns.boxplot(x="Algorithm",
                  y="Delay (ms)",
                  data=data,
                  width=0.4,
                  linewidth=1.0,
                  palette="Set2",
                  saturation=0.5,
                  showfliers=True,
                  fliersize=1.0,
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
#fig.legend(loc='upper center', bbox_to_anchor=(0.25, 0.9999))
#plt.ylim(bottom=40)
#plt.xlim((50,110))
plt.grid(axis="y", linestyle='-.')
plt.savefig('./82rtt1-t.pdf')
