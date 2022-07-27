import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use('cairo')
plt.figure(figsize=(10, 5))
subfig = 220

STEP = 0.5
PACKET = 1024
VINDEX = 0

colorset = ['red', '#1A6FDF', '#37AD6B', '#CC9900']
styleset = ['-.', ':', 'dashed', 'dotted']
pointset = ['o', 'v', 'D', '+']
nameset = ['app1', 'app2', 'app3', 'app4']
suffixset = ['0', '1', '2']

#BWs = [50, 70, 60, 40]
#TPs = [0, 20, 40, 60, 80]
BWs = [50]
TPs = [0, 75]
bwx, bwy = [], []
for i in range(len(BWs)):
    tmpx = np.linspace(TPs[i], TPs[i + 1], int((TPs[i + 1] - TPs[i]) / STEP),
                       False)
    tmpy = [BWs[i]] * len(tmpx)
    bwx += tmpx.tolist()
    bwy += tmpy
plt.plot(bwx, bwy, color='black', label='bandwidth', lw='2')

figparami = 0
sum = [0] * len(bwx)
for suffix in suffixset:
    file11 = '/root/ndn/proj-sep/log/multiport/nec-' + suffix + '.log'
    dqns = open(file11, 'r').readlines()
    x0, y0 = [], []
    datanum0 = [0] * 1000
    indexmax0 = 0
    for line in dqns:
        value = line.replace(' ', '').split(',')
        if (len(value) >= 3 and value[2] == 'data'):
            index0 = int(float(value[1]) / STEP)
            datanum0[index0] += 1
    xstep = 0
    maxnzx = 0
    for i in range(len(bwx)):
        tmp = (float(datanum0[i] * PACKET * 8) / (STEP * 1000 * 1000))
        if (tmp != 0):
            #tmp += (np.random.normal(0, 4 / 12) - 0.5)
            y0.append(tmp)
            x0.append(xstep)
            maxnzx = xstep
        sum[i] += tmp
        xstep += STEP
    x0.append(maxnzx + STEP)
    y0.append(0)
    #subfig += 1
    #plt.subplot(subfig)
    #plt.title(suffixset[subfig - 221])
    #plt.stackplot(x0,
    #              yc0,
    #              y0,
    #              y1,
    #              labels=[
    #                  'Path0', 'Path1 through the bottleneck',
    #                  'Path1 not through the bottleneck'
    #              ])
    plt.plot(x0,
             y0,
             label=nameset[figparami],
             color=colorset[figparami],
             ls='--',
             lw='2',
             marker=pointset[figparami],
             markersize='4.5')
    figparami += 1
print(sum)
plt.plot(bwx, sum, color='grey', lw=2)
plt.grid(which='both', axis="y", linestyle='-.')
plt.ylim(-2, 55)
plt.xlabel("time (s)")
plt.ylabel("Data transmission rate (Mbps)")
plt.legend(loc='lower right')
#plt.savefig('./mcth_bw.pdf')
