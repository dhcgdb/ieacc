import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('cairo')

STEP = 0.5
SEQINDEX = 11

#filenameset = [
#    '/root/ndn/proj-sep/log/other/ddpg_sta_afd-1.txt',
#    '/root/ndn/proj-sep/log/other/aimd_sta_afd-loss-1.txt',
#    '/root/ndn/proj-sep/log/other/ecp_sta_afd-1.txt',
#    '/root/ndn/proj-sep/log/other/dqn_sta_afd-1.txt'
#]

filenameset = [
    '/root/ndn/proj-sep/log/singleport/ddpg-drop-dynamic.log',
    '/root/ndn/proj-sep/log/singleport/aimd-drop-dynamic.log',
    '/root/ndn/proj-sep/log/singleport/ecp-drop-dynamic.log',
    '/root/ndn/proj-sep/log/singleport/dqn-drop-dynamic.log'
]

xset = [[] for _ in range(4)]
yset = [[] for _ in range(4)]


def findindex(seq, seqPoint, indexMax):
    for i in range(indexMax + 1):
        if (seq < seqPoint[i]):
            return i
    return i


filenindex = 0
for filename in filenameset:
    content = open(filename, 'r').readlines()
    x, y = xset[filenindex], yset[filenindex]
    filenindex += 1

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
    for i in range(indexMax):
        reqSeqPoint[i + 1] = reqSeqPoint[i] + reqNum[i + 1]
    for line in content:
        value = line.replace(' ', '').split(',')
        if (len(value) >= 3 and value[2] == 'timeout'):
            seq = int(value[SEQINDEX])
            index = findindex(seq, reqSeqPoint, indexMax)
            lossNum[index] += 1
    stepx = STEP / 2
    for i in range(indexMax + 1):
        x.append(stepx)
        y.append(lossNum[i] / reqNum[i])
        stepx += STEP

plt.figure(figsize=(10, 6.18))
f0, = plt.plot(xset[0], yset[0], color='red', label='IEACC', ls='-.')
f1, = plt.plot(xset[1], yset[1], color='#1A6FDF', label='ICP', ls=':')
f2, = plt.plot(xset[2], yset[2], color='#37AD6B', label='ECP', ls='dashed')
f3, = plt.plot(xset[3], yset[3], color='#CC9900', label='DRL-CCP', ls='dotted')
plt.legend(handles=[f0, f1, f2, f3],
           labels=['IEACC', 'ICP', 'ECP', 'DRL-CCP'],
           loc='upper right')

plt.grid(axis="y", linestyle='-.')
#plt.ylim(top=0.05)
plt.xlabel("Time (s)")
plt.ylabel("LossRate")
plt.savefig('./loss-dyn.png')
