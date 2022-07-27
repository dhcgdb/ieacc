import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('cairo')
plt.figure(figsize=(10, 6.18))
subfig = 220

STEP = 0.5
PACKET = 1024
VINDEX = 0

colorset = ['red', '#1A6FDF', '#37AD6B', '#CC9900']
styleset = ['-.', ':', 'dashed', 'dotted']
nameset = ['IEACC', 'ICP', 'ECP', 'DRL-CCP']
suffixset = ['ddpg', 'aimd', 'ecp', 'dqn']
#suffixset = ['64', '73', '82', '91','100']

figparami = 0
for suffix in suffixset:
    xc0, yc0 = [], []
    filename = '/root/ndn/proj-sep/log/singleport/' + suffix + '-drop-dynamic.log'
    with open(filename, 'r') as filep:
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

    file11 = '/root/ndn/proj-sep/log/multiport/' + suffix + '-c1-drop-82.log'
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
            float(datanum0[i] * PACKET * 8) / (STEP * 1000 * 1000) + y1[i] +
            yc0[i])
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
    plt.plot(x0,
             y0,
             label=nameset[figparami],
             color=colorset[figparami],
             ls=styleset[figparami])
    figparami += 1
plt.grid(which='both', axis="y", linestyle='-.')
plt.ylim((0, 110))
plt.xlabel("time (s)")
plt.ylabel("Data transmission rate (Mbps)")
plt.legend(loc='lower right')
plt.savefig('./th-dyn-loss.png')
