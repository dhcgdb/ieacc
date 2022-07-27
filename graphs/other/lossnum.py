import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('cairo')
plt.figure(figsize=(10, 6.18))

STEP = 5
SEQINDEX = 11

colorset = ['red', '#1A6FDF', '#37AD6B', '#CC9900']
styleset = ['-', ':', '--', '-.']
nameset = ['IEACC', 'ICP', 'ECP', 'DRL-CCP']
suffixset = ['ddpg', 'aimd', 'ecp', 'dqn']
pointset = ['o', 'v', 'D', 's']
#suffixset = ['64', '73', '82', '91', '100']

figparami = 0
for suffix in suffixset:
    filename = '/root/ndn/proj-sep/log/other/'+ suffix +'_sta_afd-1.txt'
    #filename = '/root/ndn/proj-sep/log/multiport/ddpg-c1-drop-' + suffix + '.log'
    content = open(filename, 'r').readlines()
    x0, y0 = [], []
    lossNum = [0] * 1000
    indexMax = 0
    for line in content:
        value = line.replace(' ', '').split(',')
        if (len(value) >= 3 and value[2] == 'timeout'):
            index = int(float(value[1]) / STEP)
            if (index > indexMax): indexMax = index
            lossNum[index] += 1
    for i in range(1, len(lossNum)):
        lossNum[i] += lossNum[i - 1]
    stepx = STEP / 2
    for i in range(41):
        x0.append(stepx)
        y0.append(lossNum[i])
        stepx += STEP
    plt.plot(x0,
             y0,
             label=nameset[figparami],
             color=colorset[figparami],
             ls=styleset[figparami],
             lw=2,
             marker=pointset[figparami],
             markersize=4,
             markevery=1)
    figparami += 1
plt.tick_params(labelsize=14)
plt.grid(axis="y", linestyle='-.')
plt.xlabel("Time (s)", fontdict={"size": 14})
plt.ylabel("LossPacket (Packet)", fontdict={"size": 14})
plt.ylim(top=500)
plt.legend(loc='upper left', prop={"size": 14})
plt.savefig('./lossnum-static.png')
