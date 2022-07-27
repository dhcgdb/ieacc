import matplotlib
import numpy as np
import matplotlib.pyplot as plt

matplotlib.use('cairo')
plt.figure(figsize=(8, 6.18))
subfig = 220

STEP = 10
PACKET = 1024
VINDEX = 0

colorset = ['red', '#1A6FDF', '#37AD6B', '#CC9900']
styleset = ['-', ':', '--', '-.']
nameset = ['IEACC', 'ICP', 'ECP', 'DRL-CCP']
prefixset = ['ddpg', 'aimd', 'ecp', 'dqn']
pointset = ['o', 'v', 'D', 's']
#suffixset = ['64', '73', '82', '91','100']

figparami = 0
for prefix in prefixset:
    x = [[] for _ in range(5)]
    y = [[] for _ in range(5)]
    for suffix in range(5):
        filename = '/root/ndn/proj-sep/log/singleport/' + \
            prefix + '-drop-c-' + str(suffix) + '.log'
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
                x[suffix].append(xstep)
                y[suffix].append(
                    float(datanum0[i] * PACKET * 8) / (STEP * 1000 * 1000))
                xstep += STEP
    ymeans, yerrps, yerrns = [], [], []
    for i in range(len(x[0])):
        yset = []
        for j in range(5):
            yset.append(y[j][i])
        ymean = np.mean(yset)
        yerrps.append(np.max(yset) - ymean)
        yerrns.append(ymean - np.min(yset))
        ymeans.append(ymean)

    plt.errorbar(x=x[0],
                 y=ymeans,
                 yerr=[yerrns, yerrps],
                 barsabove=True,
                 capsize=3,
                 errorevery=1,
                 elinewidth=1,
                 label=nameset[figparami],
                 color=colorset[figparami],
                 ls=styleset[figparami],
                 lw=4,
                 marker=pointset[figparami],
                 markersize=6,
                 markevery=1)
    figparami += 1
plt.grid(which='both', axis="y", linestyle='-.')
#plt.ylim()
plt.xlabel("time (s)")
plt.ylabel("Data transmission rate (Mbps)")
plt.legend(loc='lower right')
plt.savefig('./th-sta-err2.png')
