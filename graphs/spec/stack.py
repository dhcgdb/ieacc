import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('cairo')
plt.figure(figsize=(15, 5))
subfig = 120

STEP = 0.5
PACKET = 1024
VINDEX = 0

nameset = ['aimd', 'ddpg']

prefixset = ['aimd', 'ddpg']

figparami = 0
for prefix in prefixset:
    xc0, yc0 = [], []
    with open('/root/ndn/proj-sep/log/spec/' + prefix + '-c0-.log',
              'r') as filep:
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
    file11 = '/root/ndn/proj-sep/log/spec/' + prefix + '-c1-.log'
    dqns = open(file11, 'r').readlines()
    x0, y0 = [], []
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
        x0.append(xstep)
        y0.append(float(datanum0[i] * PACKET * 8) / (STEP * 1000 * 1000))
        xstep += STEP

    plt.plot(xc0,yc0)
    plt.plot(x0,y0)
    subfig += 1
    plt.subplot(subfig)
    plt.title(nameset[figparami])
    #plt.stackplot(x0, yc0, y0, labels=['p0', 'p1'])
    figparami += 1
    plt.grid(which='both', axis="y", linestyle='-.')
    plt.ylim((0, 110))
    plt.xlabel("time (s)")
    plt.ylabel("Data transmission rate (Mbps)")

#plt.figlegend(labels=['P0', 'P1'],
#              loc='lower right')
plt.savefig('./l.png')
