import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('cairo')
plt.figure(figsize=(10, 6.18))
subfig = 220

STEP = 0.5
PACKET = 1024
VINDEX = 0

#colorset = ['red', '#1A6FDF', '#37AD6B', '#CC9900','blue']
#styleset = ['-.', ':', 'dashed', 'dotted','--']
nameset = ['6:4', '7:3', '8:2', '9:1', '10:0']
suffixset = ['64', '64-2']

figparami = 0
for suffix in suffixset:
    xc0, yc0 = [], []
    with open(
            '/root/ndn/proj-sep/log/multiport/ddpg-c0-drop-test-' + suffix +
            '.log', 'r') as filep:
        dqns = filep.readlines()
        datanum0 = [0] * 1000
        indexmax0 = 0
        for line in dqns:
            value = line.replace(' ', '').split(',')
            if (len(value) >= 3 and value[2] == 'data'):
                index0 = int(float(value[1]) / STEP)
                if index0 > indexmax0: indexmax0 = index0
                datanum0[index0] += 1
        xstep = STEP / 2
        for i in range(indexmax0 + 1):
            xc0.append(xstep)
            yc0.append(float(datanum0[i] * PACKET * 8) / (STEP * 1000 * 1000))
            xstep += STEP

    file11 = '/root/ndn/proj-sep/log/multiport/ddpg-c1-drop-test-' + suffix + '.log'
    dqns = open(file11, 'r').readlines()
    x0, y0 = [], []
    x1, y1 = [], []
    datanum0 = [0] * 1000
    indexmax0 = 0
    datanum1 = [0] * 1000
    indexmax1 = 0
    for line in dqns:
        value = line.replace(' ', '').split(',')
        if (len(value) >= 3 and value[2] == 'data'):
            if (value[5] == '/ustc/1'):
                index0 = int(float(value[1]) / STEP)
                if index0 > indexmax0: indexmax0 = index0
                datanum0[index0] += 1
            elif (value[5] == '/ustc/2'):
                index1 = int(float(value[1]) / STEP)
                if index1 > indexmax1: indexmax1 = index1
                datanum1[index1] += 1
    xstep = STEP / 2
    for i in range(indexmax0 + 1):
        x1.append(xstep)
        y1.append(float(datanum1[i] * PACKET * 8) / (STEP * 1000 * 1000))
        x0.append(xstep)
        y0.append(
            float(datanum0[i] * PACKET * 8) / (STEP * 1000 * 1000) + yc0[i] +
            y1[i])
        xstep += STEP

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
    subfig += 1
    #plt.subplot(subfig)
    plt.plot(x0, y0)
    figparami += 1
plt.grid(which='both', axis="y", linestyle='-.')
plt.ylim(0, 90)
plt.xlabel("time (s)")
plt.ylabel("Data transmission rate (Mbps)")
plt.legend(loc='lower right')
plt.savefig('./ddpg64-2.png')
