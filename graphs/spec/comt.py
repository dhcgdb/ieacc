import matplotlib

matplotlib.use('cairo')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.figure(figsize=(4.5, 4.0))

colorset = ['red', '#1A6FDF', '#37AD6B', '#CC9900']
styleset = ['-', ':', '--', '-.']
nameset = ['IEACC', 'ICP', 'ECP', 'DRL-CCP']
prefixset = ['ddpg', 'aimd', 'ecp', 'dqn']
pointset = ['o', 'v', 'D', 's']


def getKey(elem):
    if (len(elem) > 3 and elem[0] == 'time'):
        return float(elem[1])
    else:
        return float('inf')


prefixset = ['ddpg', 'aimd', 'ecp', 'dqn']
#X=[50000,100000,150000,200000,250000,300000,350000,400000,450000,500000,550000,600000]#,650000]#,700000,750000,800000]
x = [i * 50000 for i in range(1, 6)]
print(x)
figparami = 0
for prefix in prefixset:
    x_ = [[] for _ in range(1)]
    y = [[] for _ in range(1)]
    for suffix in range(1):
        filename1 = '/root/ndn/proj-sep/log/spec/delay-' + \
                prefix + '.log'
        num = 0
        tocompindex = 0
        lines = open(filename1, 'r').readlines()
        valueset = []
        for line in lines:
            value = line.replace(' ', '').split(',')
            valueset.append(value)
        #valueset.sort(key=getKey)
        for value in valueset:
            if (len(value) >= 3 and value[2] == 'data'):
                num += 1
                if (num == x[tocompindex]):
                    x_[suffix].append(x[tocompindex])
                    y[suffix].append(float(value[1]))
                    tocompindex += 1
                    if (tocompindex == len(x)): break
    ymeans, yerrps, yerrns = [], [], []
    for i in range(len(x_[0])):
        yset = []
        for j in range(1):
            yset.append(y[j][i])
        ymean = np.mean(yset)
        yerrps.append(np.max(yset) - ymean)
        yerrns.append(ymean - np.min(yset))
        ymeans.append(ymean)
    print(prefix, ymeans)
    plt.errorbar(x_[0],
                 ymeans,
                 yerr=[yerrns, yerrps],
                 barsabove=True,
                 capsize=3,
                 errorevery=1,
                 elinewidth=1,
                 label=nameset[figparami],
                 color=colorset[figparami],
                 ls=styleset[figparami],
                 lw=1,
                 marker=pointset[figparami],
                 markersize=3,
                 markevery=1)
    figparami += 1

#f5, = plt.plot(x, y, color='slategrey', label='Bandwidth', ls='-')
#ax.plot(y1,color='black',linestyle='-')

plt.legend()
#plt.ylim((3,10))
#ax.legend()
#plt.grid(axis="y")

plt.grid(axis="y", linestyle='-.')
plt.xlabel("Data number")
plt.ylabel("Completion time (s)")

#plt.xlim((0,6000))
#plt.savefig('./acomp.png')
#plt.show()
