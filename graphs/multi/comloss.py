import matplotlib

matplotlib.use('cairo')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def getKey(elem):
    if (len(elem) > 3 and elem[0] == 'time'):
        return float(elem[1])
    else:
        return float('inf')


prefixset = ['ddpg', 'aimd', 'ecp', 'dqn']
TPBASE = 20
TPNUM = 10
#X=[50000,100000,150000,200000,250000,300000,350000,400000,450000,500000,550000,600000]#,650000]#,700000,750000,800000]
timepoint = [TPBASE * (i + 1) for i in range(TPNUM)]
y = [[0] * TPNUM for _ in range(len(prefixset))]
print(timepoint)
print(y)

index = 0
for prefix in prefixset:
    #filename1 = '/root/ndn/proj-sep/log/multiport/' + prefix + '-c1-drop-82.log'
    #filename2 = '/root/ndn/proj-sep/log/multiport/' + prefix + '-c0-drop-82.log'
    filename1 = '/root/ndn/proj-sep/log/other/' + prefix + '_sta_afd-1.txt'
    num = 0
    tocompindex = 0
    lines = open(filename1,
                 'r').readlines()  #+ open(filename2, 'r').readlines()
    valueset = []
    for line in lines:
        value = line.replace(' ', '').split(',')
        valueset.append(value)
    #valueset.sort(key=getKey)
    listonce = y[index]
    for value in valueset:
        if (len(value) >= 3 and value[2] == 'timeout'):
            listonce[int(float(value[1]) / TPBASE)] += 1
    for i in range(TPNUM - 1):
        listonce[i + 1] += listonce[i]
    index += 1
print(y)

plt.figure(figsize=(8, 4.0))

f1, = plt.plot(timepoint,
               y[0],
               color='#1A6FDF',
               marker='+',
               label='IEACC',
               ls='-.')
f2, = plt.plot(timepoint,
               y[1],
               color='#37AD6B',
               marker='*',
               label='ICP',
               ls=':')
f3, = plt.plot(timepoint,
               y[2],
               color='#B177DE',
               marker='D',
               label='ECP',
               ls='dashed')
f4, = plt.plot(timepoint,
               y[3],
               color='#CC9900',
               marker='o',
               label='DRL-CCP',
               ls='dotted')
#f5, = plt.plot(x, y, color='slategrey', label='Bandwidth', ls='-')
#ax.plot(y1,color='black',linestyle='-')

plt.legend(
    handles=[f1, f2, f3, f4],
    labels=['IEACC', 'ICP', 'ECP', 'DRL-CCP'],
)
#plt.ylim((3,10))
#ax.legend()
#plt.grid(axis="y")

plt.grid(axis="y", linestyle='-.')
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(20))
plt.xlabel("Time(s)")
plt.ylabel("Loss Packet Number(Packet)")
plt.savefig('./lcomp.png')
