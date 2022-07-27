import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('cairo')
plt.figure(figsize=(10, 6.18))

STEP = 0.5
SEQINDEX = 11


def findindex(seq, seqPoint, indexMax):
    for i in range(indexMax + 1):
        if (seq < seqPoint[i]):
            return i
    return i


colorset = ['red', '#1A6FDF', '#37AD6B', '#CC9900']
styleset = ['-.', ':', 'dashed', 'dotted']
nameset = ['IEACC', 'ICP', 'ECP', 'DRL-CCP']
suffixset = ['ddpg', 'aimd', 'ecp', 'dqn']
#suffixset = ['64', '73', '82', '91', '100']

figparami = 0
for suffix in suffixset:
    filename = '/root/ndn/proj-sep/log/singleport/' + suffix + '-drop-dynamic.log'
    #filename = '/root/ndn/proj-sep/log/multiport/ddpg-c1-drop-' + suffix + '.log'
    content = open(filename, 'r').readlines()
    x0, y0 = [], []
    reqNum = [0] * 1000
    reqSeqPoint = [0] * 1000
    lossNum = [0] * 1000
    indexMax = 0
    for line in content:
        value = line.replace(' ', '').split(',')
        if (len(value) >= 3 and value[2] == 'req'):
            index = int(float(value[1]) / STEP)
            if index > indexMax: indexMax = index
            reqNum[index] += 1
    reqSeqPoint[0] = reqNum[0]
    for i in range(1, indexMax + 1):
        reqSeqPoint[i] = reqSeqPoint[i - 1] + reqNum[i]
    for line in content:
        value = line.replace(' ', '').split(',')
        if (len(value) >= 3 and value[2] == 'timeout'):
            seq = int(value[SEQINDEX])
            index = findindex(seq, reqSeqPoint, indexMax)
            lossNum[index] += 1
    stepx = STEP / 2
    for i in range(indexMax + 1):
        x0.append(stepx)
        y0.append(lossNum[i] / reqNum[i])
        stepx += STEP
    plt.plot(x0,
             y0,
             label=nameset[figparami],
             color=colorset[figparami],
             ls=styleset[figparami])
    figparami += 1
plt.grid(axis="y", linestyle='-.')
plt.xlabel("Time (s)")
plt.ylabel("LossRate")
plt.ylim(bottom=-0.00025)
plt.legend()
plt.savefig('./loss-dyn.png')
