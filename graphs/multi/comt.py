import matplotlib

matplotlib.use('cairo')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#filename_1 = '/root/ndn/proj-sep/log/other/ddpg_dyn_afd-1.txt'
#filename_2 = '/root/ndn/proj-sep/log/other/aimd_dyn_afd-1.txt'
#filename_3 = '/root/ndn/proj-sep/log/other/ecp_dyn_afd-1.txt'
#filename_4 = '/root/ndn/proj-sep/log/other/dqn_dyn_afd-1.txt'


def getKey(elem):
    if (len(elem) > 3 and elem[0] == 'time'):
        return float(elem[1])
    else:
        return float('inf')


a = [[28.810917068, 54.682472405, 80.536902644, 106.404895152, 132.276846488],
     [38.551888968, 76.161268984, 113.492668901, 152.995662648, 190.023194419],
     [33.528838619, 65.977250076, 98.659929152, 131.075539816, 163.750608081],
     [29.922226244, 55.754918723, 81.591961551, 107.431267245, 133.26518145]]
prefixset = ['ddpg', 'aimd', 'ecp', 'dqn']
#X=[50000,100000,150000,200000,250000,300000,350000,400000,450000,500000,550000,600000]#,650000]#,700000,750000,800000]
x = [150000, 300000, 450000, 600000, 750000]
y = [[] for _ in range(len(prefixset))]

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
    for value in valueset:
        if (len(value) >= 3 and value[2] == 'data'):
            num += 1
            if (num == x[tocompindex]):
                y[index].append(float(value[1]))
                tocompindex += 1
                if (tocompindex == len(x)): break
    index += 1

print(y)

plt.figure(figsize=(4.5, 4.0))

f1, = plt.plot(x, y[0], color='#1A6FDF', marker='+', label='IEACC', ls='-.')
f2, = plt.plot(x, y[1], color='#37AD6B', marker='*', label='ICP', ls=':')
f3, = plt.plot(x, y[2], color='#B177DE', marker='D', label='ECP', ls='dashed')
f4, = plt.plot(x,
               y[3],
               color='#CC9900',
               marker='o',
               label='DRL-CCP',
               ls='dotted')
#f5, = plt.plot(x, y, color='slategrey', label='Bandwidth', ls='-')
#ax.plot(y1,color='black',linestyle='-')

plt.legend(handles=[f1, f2, f3, f4],
           labels=['IEACC', 'ICP', 'ECP', 'DRL-CCP'],
           loc='lower right')
#plt.ylim((3,10))
#ax.legend()
#plt.grid(axis="y")

plt.grid(axis="y", linestyle='-.')
plt.xlabel("Data number")
plt.ylabel("Completion time (s)")

#plt.xlim((0,6000))
plt.savefig('./acomp.png')
#plt.show()
