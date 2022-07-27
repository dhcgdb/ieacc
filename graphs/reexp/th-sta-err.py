import matplotlib
import numpy as np
import matplotlib.pyplot as plt

matplotlib.use('cairo')
plt.figure(figsize=(10, 6.18))
subfig = 220

STEP = 2
PACKET = 1024
VINDEX = 0
item = 'ddpg'
colorset = ['violet', '#1A6FDF', '#37AD6B', '#CC9900', 'red']
styleset = [(0, (3, 1, 1, 1)), '--', ':', '-.', '-']
nameset = ['6:4', '7:3', '8:2', '9:1', '10:0']
prefixset = ['64', '73', '82', '91', '100']
pointset = ['o', 'v', 'D', 's', '^']

xc0 = [[] for _ in range(5)]
yc0 = [[] for _ in range(5)]
for suffix in range(5):
    filename = '/root/ndn/proj-sep/log/reexp/' +\
            item+'-c0-' + str(suffix) + '.log'
    with open(filename, 'r') as filep:
        lines = filep.readlines()
        datanum0 = [0] * 1000
        indexmax0 = 0
        for line in lines:
            value = line.replace(' ', '').split(',')
            if (len(value) >= 3 and value[2] == 'data'):
                index0 = int(float(value[1]) / STEP)
                if index0 > indexmax0: indexmax0 = index0
                datanum0[index0] += 1
        xstep = STEP / 2
        for i in range(indexmax0 + 1):
            xc0[suffix].append(xstep)
            yc0[suffix].append(
                float(datanum0[i] * PACKET * 8) / (STEP * 1000 * 1000))
            xstep += STEP
for i in range(5):
    print(np.mean(yc0))
figparami = 0
for prefix in prefixset:
    x = [[] for _ in range(5)]
    y1 = [[] for _ in range(5)]
    y2 = [[] for _ in range(5)]
    for suffix in range(5):
        filename = '/root/ndn/proj-sep/log/reexp/' +\
             item+'-c1-' + prefix + '-'+str(suffix) + '.log'
        with open(filename, 'r') as filep:
            lines = filep.readlines()
            datanum0 = [0] * 1000
            datanum1 = [0] * 1000
            indexmax0 = 0
            for line in lines:
                value = line.replace(' ', '').split(',')
                if (len(value) >= 3 and value[2] == 'data'):
                    index0 = int(float(value[1]) / STEP)
                    if index0 > indexmax0: indexmax0 = index0
                    if (value[5] == '/ustc/1'):
                        datanum0[index0] += 1
                    if (value[5] == '/ustc/2'):
                        datanum1[index0] += 1
            xstep = STEP / 2
            for i in range(indexmax0 + 1):
                x[suffix].append(xstep)
                y1[suffix].append(
                    float(datanum0[i] * PACKET * 8) / (STEP * 1000 * 1000))
                y2[suffix].append(
                    float(datanum1[i] * PACKET * 8) / (STEP * 1000 * 1000))
                xstep += STEP
    print(prefix)
    print(np.mean(y1))
    print(np.mean(y2))
#    ymeans, yerrps, yerrns, yvars = [], [], [], []
#    for i in range(len(x[0])):
#        yset = []
#        for j in range(5):
#            yset.append(y[j][i])
#        ymean = np.mean(yset)
#        yerrps.append(np.max(yset) - ymean)
#        yerrns.append(ymean - np.min(yset))
#        yvars.append(np.var(yset))
#        ymeans.append(ymean)
#    plt.errorbar(x=x[0],
#                 y=ymeans,
#                 yerr=[yerrns, yerrps],
#                 barsabove=True,
#                 capsize=3,
#                 errorevery=1,
#                 elinewidth=0.5,
#                 label=nameset[figparami],
#                 color=colorset[figparami],
#                 ls=styleset[figparami],
#                 lw=1,
#                 marker=pointset[figparami],
#                 markersize=3,
#                 markevery=1)
#    figparami += 1

plt.grid(which='both', axis="y", linestyle='-.')
plt.ylim(top=110)
plt.tick_params(labelsize=14)
plt.xlabel("Time (s)", fontdict={"size": 14})
plt.ylabel("Data transmission rate (Mbps)", fontdict={"size": 14})
plt.legend(loc='lower right', prop={"size": 14})
#plt.savefig('./' + item + '-err.pdf')
