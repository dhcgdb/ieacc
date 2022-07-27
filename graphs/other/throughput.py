import matplotlib

matplotlib.use('cairo')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

filename_1 = '/root/ndn/proj-sep/log/singleport/ddpg-drop-dynamic.log'
filename_2 = '/root/ndn/proj-sep/log/singleport/aimd-drop-dynamic.log'
filename_3 = '/root/ndn/proj-sep/log/singleport/ecp-drop-dynamic.log'
filename_4 = '/root/ndn/proj-sep/log/singleport/dqn-drop-dynamic.log'

#filename_1 = '/root/ndn/proj-sep/log/other/ddpg_dyn_afd-1.txt'
#filename_2 = '/root/ndn/proj-sep/log/other/aimd_dyn_afd-1.txt'
#filename_3 = '/root/ndn/proj-sep/log/other/ecp_dyn_afd-1.txt'
#filename_4 = '/root/ndn/proj-sep/log/other/dqn_dyn_afd-1.txt'

#filename_1 = '/root/ndn/proj-sep/log/other/ddpg_sta_afd-1.txt'
#filename_2 = '/root/ndn/proj-sep/log/other/aimd_sta_afd-loss-1.txt'
#filename_3 = '/root/ndn/proj-sep/log/other/ecp_sta_afd-1.txt'
#filename_4 = '/root/ndn/proj-sep/log/other/dqn_sta_afd-1.txt'

X, Y_1, Y_2, Y_3, Y_4 = [], [], [], [], []

step = 0.5
datanum = 0
step1 = step
packet = 1024
with open(filename_1, 'r') as f:
    lines = f.readlines()
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if (len(value) == 20):
            t = float(value[1])
            if (t < step1):
                datanum = datanum + 1
                #num = num+1
            else:
                a = float(datanum * packet * 8) / (step * 1000 * 1000)
                Y_1.append(a)
                step1 = step1 + step
                X.append(t)
                datanum = 0
datanum = 0
t = 0
step1 = step
with open(filename_2, 'r') as f:
    lines = f.readlines()
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if (len(value) == 20):
            t = float(value[1])
            if (t < step1):
                datanum = datanum + 1
                #num = num+1
            else:
                a = float(datanum * packet * 8) / (step * 1000 * 1000)
                Y_2.append(a)
                step1 = step1 + step
                datanum = 0

datanum = 0
t = 0
step1 = step
with open(filename_3, 'r') as f:
    lines = f.readlines()
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if (len(value) == 20):
            t = float(value[1])
            if (t < step1):
                datanum = datanum + 1
                #num = num+1
            else:
                a = float(datanum * packet * 8) / (step * 1000 * 1000)
                Y_3.append(a)
                step1 = step1 + step
                datanum = 0
datanum = 0
t = 0
step1 = step
with open(filename_4, 'r') as f:
    lines = f.readlines()
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if (len(value) == 20):
            t = float(value[1])
            if (t < step1):
                datanum = datanum + 1
                #num = num+1
            else:
                a = float(datanum * packet * 8) / (step * 1000 * 1000)
                Y_4.append(a)
                step1 = step1 + step
                datanum = 0

#plt.plot([Y_1,Y_2,Y_3])
#fig,ax = plt.subplots()
#x = np.linespace(0,200,100)
x = np.linspace(0, 50, 50)
y1 = 73.7
m = 1999

print(len(Y_1), len(Y_2), len(Y_3), len(Y_4))
X = X[0:m]
plt.figure(figsize=(10, 6.18))

xxx = np.linspace(0, 200, 2000, endpoint=False)
BW = [
    50, 30, 48, 28, 50, 36, 48, 31, 49, 35, 28, 48, 38, 49, 40, 31, 49, 40, 29,
    38, 47
]
TP = [
    0, 12, 20, 30, 42, 50, 58, 70, 80, 84, 90, 105, 110, 116, 130, 140, 157,
    170, 180, 185, 193, 200
]
yyy = [0] * len(xxx)
print(xxx, yyy)
#indexy = 0
#for t in range(0, 21):
#    for k in range(0, (TP[t + 1] - TP[t]) * 5):
#        yyy[indexy] = BW[t]
#        indexy += 1
indexy = 0
beginbw = 50
endbw = 50
for t in range(21):
    if (t != 0): beginbwbw = BW[t - 1]
    endbw = BW[t]
    diff = beginbw - endbw
    while (beginbw != endbw):
        if (diff > 0): beginbw -= 1
        else: beginbw += 1
        yyy[indexy] = beginbw
        indexy += 1
    if (diff < 0): diff = -diff
    for _ in range((TP[t + 1] - TP[t]) * 10 - diff):
        yyy[indexy] = BW[t]
        indexy += 1

f1, = plt.plot(X[0:m], Y_1[0:m], lw=1.5, color='red', label='IEACC', ls='--')
f2, = plt.plot(X[0:m], Y_2[0:m], lw=1.5, color='#1A6FDF', label='ICP', ls='-.')
f3, = plt.plot(X[0:m], Y_3[0:m], lw=1.5, color='#37AD6B', label='ECP',
               ls=':')  #B177DE
f4, = plt.plot(X[0:m],
               Y_4[0:m],
               lw=1.5,
               color='#CC9900',
               label='DRL-CCP',
               ls=(0, (3, 1, 1, 1)))
#f5, = plt.plot(xxx, yyy, lw=1.5, color='lightgrey', label='Bandwidth', ls='-')
#ax.plot(y1,color='black',linestyle='-')

plt.legend(handles=[f1, f2, f3, f4],
           labels=['IEACC', 'ICP', 'ECP', 'DRL-CCP'],
           loc='lower right',
           prop={"size": 16})
#plt.ylim((3,10))
#ax.legend()
#plt.grid(axis="y")

plt.tick_params(labelsize=16)
plt.grid(axis="y", linestyle='-.')
plt.xlabel("time (s)", fontdict={"size": 16})
plt.ylabel("Data transmission rate (Mbps)", fontdict={"size": 16})

#plt.xlim((0,6000))
#plt.savefig('./A_th_sta.jpg')
plt.savefig('./A_th_sta_bw_3.pdf')
#plt.show()