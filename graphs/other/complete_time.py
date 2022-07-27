import matplotlib

matplotlib.use('cairo')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#filename_1 = '/root/ndn/proj-sep/log/other/ddpg_dyn_afd-1.txt'
#filename_2 = '/root/ndn/proj-sep/log/other/aimd_dyn_afd-1.txt'
#filename_3 = '/root/ndn/proj-sep/log/other/ecp_dyn_afd-1.txt'
#filename_4 = '/root/ndn/proj-sep/log/other/dqn_dyn_afd-1.txt'

filename_1 = '/root/ndn/proj-sep/log/multiport/ddpg-c1-drop-82.log'
filename_2 = '/root/ndn/proj-sep/log/multiport/aimd-c1-drop-82.log'
filename_3 = '/root/ndn/proj-sep/log/multiport/ecp-c1-drop-82.log'
filename_4 = '/root/ndn/proj-sep/log/multiport/dqn-c1-drop-82.log'

X, Y_1, Y_2, Y_3, Y_4 = [], [], [], [], []

#X=[50000,100000,150000,200000,250000,300000,350000,400000,450000,500000,550000,600000]#,650000]#,700000,750000,800000]
X = [25000, 50000, 75000, 100000, 125000]
W = []
num = 0
n = 0
with open(filename_1, 'r') as f:
    lines = f.readlines()
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if (len(value) == 20):
            num = num + 1
            for n in range(0, len(X)):
                if (num == float(X[n])):
                    Y_1.append(float(value[1]))

W.clear()
num = 0
with open(filename_2, 'r') as f:
    lines = f.readlines()
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if (len(value) == 20):
            num = num + 1
            for n in range(0, len(X)):
                if (num == float(X[n])):
                    Y_2.append(float(value[1]))

W.clear()
num = 0
with open(filename_3, 'r') as f:
    lines = f.readlines()
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if (len(value) == 20):
            num = num + 1
            for n in range(0, len(X)):
                if (num == float(X[n])):
                    Y_3.append(float(value[1]))

num = 0
with open(filename_4, 'r') as f:
    lines = f.readlines()
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if (len(value) == 20):
            num = num + 1
            for n in range(0, len(X)):
                if (num == float(X[n])):
                    Y_4.append(float(value[1]))

print(Y_1,Y_2,Y_3,Y_4)

plt.figure(figsize=(4.5, 4.0))

f1, = plt.plot(X, Y_1, color='#1A6FDF', marker='+', label='IEACC', ls='-.')
f2, = plt.plot(X, Y_2, color='#37AD6B', marker='*', label='ICP', ls=':')
f3, = plt.plot(X, Y_3, color='#B177DE', marker='D', label='ECP', ls='dashed')
f4, = plt.plot(X,
               Y_4,
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
