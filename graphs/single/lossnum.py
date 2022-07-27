import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('cairo')
plt.figure(figsize=(10, 6.18))

STEP = 2.5
SEQINDEX = 11

colorset = ['red', '#1A6FDF', '#37AD6B', '#CC9900']
styleset = ['-', ':', '--', '-.']
nameset = ['IEACC', 'ICP', 'ECP', 'DRL-CCP']
suffixset = ['ddpg', 'aimd', 'ecp', 'dqn']
pointset = ['o', 'v', 'D', 's']
#suffixset = ['64', '73', '82', '91', '100']

figparami = 0
for suffix in suffixset:
    #filename = '/root/ndn/proj-sep/log/singleport/' + suffix + '-drop-c-4.log'
    filename = '/root/ndn/proj-sep/log/singleport/' + suffix + '-drop-dynamic.log'
    #if (suffix == 'aimd'):
        #filename = '/root/ndn/proj-sep/log/singleport/aimd-drop-c-2.log'
    print(filename)
    #filename = '/root/ndn/proj-sep/log/multiport/ddpg-c1-drop-' + suffix + '.log'
    content = open(filename, 'r').readlines()
    x0, y0 = [], []
    dataNum=[0]*1000
    lossNum = [0] * 1000
    indexMax = 0
    for line in content:
        value = line.replace(' ', '').split(',')
        if (len(value) >= 3 and value[2] == 'data'):
            index = int(float(value[1]) / STEP)
            if (index > indexMax): indexMax = index
            dataNum[index] += 1
        if (len(value) >= 3 and value[2] == 'timeout'):
            index = int(float(value[1]) / STEP)
            if (index > indexMax): indexMax = index
            lossNum[index] += 1
    #for i in range(1, len(lossNum)):
    #    lossNum[i] += lossNum[i - 1]
    #if (suffix == 'ddpg'):
    #    for i in range(len(lossNum)):
    #        lossNum[i] = 0
    stepx = STEP / 2
    a = open('./lossrate-dyn-' + suffix + '.txt', 'w')
    for i in range(indexMax + 1):
        x0.append(stepx)
        #if (suffix == 'aimd'):
        #    lossNum[i] = (1.02 * stepx + 46) / (0.285 * stepx +
        #                                        57) * lossNum[i]
        y0.append(lossNum[i]/dataNum[i])
        a.write(str(stepx) + ',' + str(lossNum[i]/dataNum[i]) + '\n')
        stepx += STEP
    a.close()
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
plt.tick_params(labelsize=16)
plt.grid(axis="y", linestyle='-.')
plt.xlabel("Time (s)", fontdict={"size": 16})
plt.ylabel("LossPacket (Packet)", fontdict={"size": 16})
plt.ylim()
plt.legend(loc='upper left', prop={"size": 16})
plt.savefig('./lossrate-dynamic-drop-00-num.png')
