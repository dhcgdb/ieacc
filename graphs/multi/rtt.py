import matplotlib

matplotlib.use('cairo')
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from numpy.core.fromnumeric import mean

STEP = 0.5
PACKET = 1024
VINDEX = 17

file11 = '/root/ndn/proj-sep/log/multiport/aimd-c0.log'
file12 = '/root/ndn/proj-sep/log/multiport/aimd-c1.log'
file13 = '/root/ndn/proj-sep/log/multiport/aimd-c2.log'
y1 = []
aimdc0 = open(file11, 'r').readlines()
aimdc1 = open(file12, 'r').readlines()
aimdc2 = open(file13, 'r').readlines()
aimds = aimdc1
for line in aimds:
    value = line.replace(' ', '').split(',')
    if (len(value) >= 3 and value[2] == 'data'):
        y1.append(float(value[VINDEX]) * 1000)

file21 = '/root/ndn/proj-sep/log/multiport/ecp-c0.log'
file22 = '/root/ndn/proj-sep/log/multiport/ecp-c1.log'
file23 = '/root/ndn/proj-sep/log/multiport/ecp-c2.log'
y2 = []
ecpc0 = open(file21, 'r').readlines()
ecpc1 = open(file22, 'r').readlines()
ecpc2 = open(file23, 'r').readlines()
ecps = ecpc1
for line in ecps:
    value = line.replace(' ', '').split(',')
    if (len(value) >= 3 and value[2] == 'data'):
        y2.append(float(value[VINDEX]) * 1000)

file31 = '/root/ndn/proj-sep/log/multiport/dqn-c0.log'
file32 = '/root/ndn/proj-sep/log/multiport/dqn-c1.log'
file33 = '/root/ndn/proj-sep/log/multiport/dqn-c2.log'
y3 = []
dqnc0 = open(file31, 'r').readlines()
dqnc1 = open(file32, 'r').readlines()
dqnc2 = open(file33, 'r').readlines()
dqns = dqnc1
for line in dqns:
    value = line.replace(' ', '').split(',')
    if (len(value) >= 3 and value[2] == 'data'):
        y3.append(float(value[VINDEX]) * 1000)

file41 = '/root/ndn/proj-sep/log/multiport/ddpg-c0.log'
file42 = '/root/ndn/proj-sep/log/multiport/ddpg-c1.log'
file43 = '/root/ndn/proj-sep/log/multiport/ddpg-c2.log'
y4 = []
ddpgc0 = open(file41, 'r').readlines()
ddpgc1 = open(file42, 'r').readlines()
ddpgc2 = open(file43, 'r').readlines()
ddpgs = ddpgc1
for line in ddpgs:
    value = line.replace(' ', '').split(',')
    if (len(value) >= 3 and value[2] == 'data'):
        y4.append(float(value[VINDEX]) * 1000)

y = y4 + y1 + y2 + y3
x = ['IEACC'] * len(y4) + ['ICP'] * len(y1) + ['ECP'] * len(y2) + ['DRL-CCP'
                                                                   ] * len(y3)
print(len(y), len(x))

from pandas.core.frame import DataFrame

data = {"Algorithm": x, "Delay (ms)": y}  #将列表a，b转换成字典
data = DataFrame(data)  #将字典转换成为数据框

plt.figure(figsize=(8, 5))
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
fig.legend(loc='upper center', bbox_to_anchor=(0.25, 0.9999))

#plt.ylim((40,250))
#plt.xlim((50,110))
#params = {'figure.figsize':'6,5'}
#plt.rcParams.update(params)
plt.grid(axis="y", linestyle='-.')
plt.savefig('./rttc1.png')
