import matplotlib
matplotlib.use('cairo')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#filename_1 = '/root/ndn/proj-sep/ddpg_dym-1.txt'
#filename_2 = '/root/ndn/proj-sep/aimd_dym-1.txt'
#filename_3 = '/root/ndn/proj-sep/ecp_dyn_afd-1.txt'
#filename_4 = '/root/ndn/proj-sep/dqn_dym-1.txt'

#filename_1 = '/root/ndn/proj-sep/log/other/ddpg_dyn_afd-1.txt'
#filename_2 = '/root/ndn/proj-sep/log/other/aimd_dyn_afd-1.txt'
#filename_3 = '/root/ndn/proj-sep/log/other/ecp_dyn_afd-1.txt'
#filename_4 = '/root/ndn/proj-sep/log/other/dqn_dyn_afd-1.txt'

filename_1 = '/root/ndn/proj-sep/log/other/ddpg_sta_afd-1.txt'
filename_2 = '/root/ndn/proj-sep/log/other/aimd_sta_afd-loss-1.txt'
filename_3 = '/root/ndn/proj-sep/log/other/ecp_sta_afd-1.txt'
filename_4 = '/root/ndn/proj-sep/log/other/dqn_sta_afd-1.txt'

X, Y_1, Y_2, Y_3, Y_4 = [], [], [], [], []

num = 0
step = 0.5
a = []
station = 7
step1 = step

with open(filename_1, 'r') as f:
    lines = f.readlines()
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if (len(value) == 20):
            t = float(value[1])
            if (t < step1):
                a.append(float(value[station]))
            else:
                Y_1.append(np.mean(a))
                step1 = step1 + step
                a.clear()
                X.append(t)
            data = value[11]
print('data:', data)
a.clear()
step1 = step

with open(filename_2, 'r') as f:
    lines = f.readlines()
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if (len(value) == 20):
            t = float(value[1])
            if (t < step1):
                a.append(float(value[station]))
            else:
                Y_2.append(np.mean(a))
                step1 = step1 + step
                a.clear()
            data = value[11]

print('data:', data)
a.clear()
step1 = step

with open(filename_3, 'r') as f:
    lines = f.readlines()
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if (len(value) == 20):
            t = float(value[1])
            if (t < step1):
                a.append(float(value[station]))
            else:
                Y_3.append(np.mean(a))
                step1 = step1 + step
                a.clear()

            data = value[11]

print('data:', data)
a.clear()
step1 = step

with open(filename_4, 'r') as f:
    lines = f.readlines()
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if (len(value) == 20):
            t = float(value[1])
            if (t < step1):
                a.append(float(value[station]))
            else:
                Y_4.append(np.mean(a))
                step1 = step1 + step
                a.clear()
            data = value[11]
print('data:', data)

#x=np.linspace(0,50,50)

m = 1999

print(len(Y_1), len(Y_2), len(Y_3), len(Y_4))
X = X[0:m]
plt.figure(figsize=(9.0, 4.5))

x = np.linspace(0, 201, 1000)
interval = [0] * 22
BW = [
    50, 30, 48, 28, 50, 36, 48, 31, 49, 35, 28, 48, 38, 49, 40, 31, 49, 40, 29,
    38, 47
]
TP = [
    0, 12, 20, 30, 42, 50, 58, 70, 80, 84, 90, 105, 110, 116, 130, 140, 157,
    170, 180, 185, 193, 200
]
for t in range(0, 21):
    interval[t] = [1 if (i > TP[t] and i < TP[t + 1]) else 0 for i in x]
y = [0] * 1000
indexy = 0
for t in range(0, 21):
    #y = y + BW[t]*interval[t]
    for k in range(0, (TP[t + 1] - TP[t]) * 5):
        y[indexy] = BW[t]*7
        indexy += 1

#f1, = plt.plot(X[0:m], Y_1[0:m], color='#1A6FDF', label='IEACC', ls='-.')
#f2, = plt.plot(X[0:m], Y_2[0:m], color='#37AD6B', label='ICP', ls=':')
#f3, = plt.plot(X[0:m], Y_3[0:m], color='#B177DE', label='ECP', ls='dashed')
#f4, = plt.plot(X[0:m], Y_4[0:m], color='#CC9900', label='DRL-CCP', ls='dotted')

f1,=plt.plot(X[0:m],Y_1[0:m],color='red',label='IEACC',ls='-.')
f2,=plt.plot(X[0:m],Y_2[0:m],color='#1A6FDF',label='ICP',ls=':')
f3,=plt.plot(X[0:m],Y_3[0:m],color='#37AD6B',label='ECP',ls='dashed')#B17
f4,=plt.plot(X[0:m],Y_4[0:m],color='#CC9900',label='DRL-CCP',ls='dotted')

#f5, = plt.plot(x, y, color='slategrey', label='Bandwidth', ls='-')
#ax.plot(y1,color='black',linestyle='-')

plt.legend(handles=[f1, f2, f3, f4],
           labels=['IEACC', 'ICP', 'ECP', 'DRL-CCP'],
           loc='lower right')
#plt.ylim((3,10))
#ax.legend()
#plt.grid(axis="y")

plt.grid(axis="y", linestyle='-.')
plt.xlabel("time (s)")
plt.ylabel("Interest request rate / cwnd")

#plt.xlim((0,6000))
plt.savefig('./A_bw_sta.pdf')
#plt.show()