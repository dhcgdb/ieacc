import matplotlib

matplotlib.use('cairo')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

filename_1 = '/root/ndn/proj-sep/log/other/ddpg_dyn_afd-1.txt'
filename_2 = '/root/ndn/proj-sep/log/other/aimd_dyn_afd-1.txt'
filename_3 = '/root/ndn/proj-sep/log/other/ecp_dyn_afd-1.txt'
filename_4 = '/root/ndn/proj-sep/log/other/dqn_dyn_afd-1.txt'

#filename_1 = '/root/ndn/proj-sep/log/other/ddpg_sta_afd-1.txt'
#filename_2 = '/root/ndn/proj-sep/log/other/aimd_sta_afd-1.txt'
#filename_3 = '/root/ndn/proj-sep/log/other/ecp_sta_afd-1.txt'
#filename_4 = '/root/ndn/proj-sep/log/other/dqn_sta_afd-1.m.txt'

X, Y_1, Y_2, Y_3, Y_4 = [], [], [], [], []

num = 0
n = 2700
a = []
station = 17
with open(filename_1, 'r') as f:
    lines = f.readlines()
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if (len(value) == 20):
            if (num < n):
                a.append(float(value[station]) * 1000)
                num = num + 1
            else:
                Y_1.append(np.mean(a))
                num = 0
                a.clear()
                X.append(float(value[station]))
            data = value[11]
            #break
num = 0
a.clear()
print("AIMD_60----total_data_transmited: ", data)

with open(filename_2, 'r') as f:
    lines = f.readlines()
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if (len(value) == 20):
            if (num < n + 2500):
                a.append(float(value[station]) * 1000)
                num = num + 1
            else:
                Y_2.append(np.mean(a))
                num = 0
                a.clear()
                X.append(float(value[1]))
            data = value[11]
print("AIMD_80---- total_data_transmited: ", data)

num = 0
a.clear()

with open(filename_3, 'r') as f:
    lines = f.readlines()
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if (len(value) == 20):
            if (num < n):
                a.append(float(value[station]) * 1000)
                num = num + 1
            else:
                Y_3.append(np.mean(a))
                num = 0
                a.clear()
                X.append(float(value[1]))
            data = value[11]
print("AIMD_100---- total_data_transmited: ", data)
num = 0
a.clear()

with open(filename_4, 'r') as f:
    lines = f.readlines()
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if (len(value) == 20):
            if (num < n):
                a.append(float(value[station]) * 1000)
                num = num + 1
            else:
                Y_4.append(np.mean(a))
                num = 0
                a.clear()
                X.append(float(value[1]))
            data = value[11]
print("ECP_60---- total_data_transmited: ", data)
num = 0
a.clear()

xf = open("./rtt-ddpg-dyn.txt", "w")
for i in range(len(Y_1)):
    xf.write(str(Y_1[i]) + '\n')
xf.close()

xf = open("./rtt-aimd-dyn.txt", "w")
for i in range(len(Y_2)):
    xf.write(str(Y_2[i]) + '\n')
xf.close()

xf = open("./rtt-ecp-dyn.txt", "w")
for i in range(len(Y_3)):
    xf.write(str(Y_3[i]) + '\n')
xf.close()

xf = open("./rtt-dqn-dyn.txt", "w")
for i in range(len(Y_4)):
    xf.write(str(Y_4[i]) + '\n')
xf.close()

y = Y_1 + Y_2 + Y_3 + Y_4
x = ['IEACC'] * len(Y_1) + ['ICP'] * len(Y_2) + ['ECP'] * len(
    Y_3) + ['DRL-CCP'] * len(Y_4)
print(len(y), len(x))

from pandas.core.frame import DataFrame

data = {"Algorithm": x, "Delay (ms)": y}  #将列表a，b转换成字典
data = DataFrame(data)  #将字典转换成为数据框

import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(4.5, 4.0))
fig = sns.boxplot(x="Algorithm",
                  y="Delay (ms)",
                  data=data,
                  width=0.4,
                  linewidth=1.0,
                  palette="Set2",
                  saturation=0.5,
                  showfliers=True,
                  fliersize=4.0,
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
fig.set_ylim(60, 70)
#fig.legend(loc='upper center',bbox_to_anchor=(0.25,0.9999))

#plt.ylim((40,250))
#plt.xlim((50,110))
#params = {'figure.figsize':'6,5'}
#plt.rcParams.update(params)
plt.grid(axis="y", linestyle='-.')
plt.savefig('./A_rtt_dyn2-t.pdf')
