import matplotlib
matplotlib.use('cairo')
import matplotlib.pyplot as plt
from numpy.core.fromnumeric import mean

STEP = 0.5
PACKET = 1024
VINDEX = 7

file11 = '/root/ndn/proj-sep/log/multiport/aimd-c0.log'
file12 = '/root/ndn/proj-sep/log/multiport/aimd-c1.log'
file13 = '/root/ndn/proj-sep/log/multiport/aimd-c2.log'
x1, y1 = [], []
aimdc0 = open(file11, 'r').readlines()
aimdc1 = open(file12, 'r').readlines()
aimdc2 = open(file13, 'r').readlines()
aimds = aimdc1
cwnd = [[] for _ in range(1000)]
indexmax = 0
for line in aimds:
    value = line.replace(' ', '').split(',')
    if (len(value) >= 3 and value[2] == 'data'):
        index = int(float(value[1]) / STEP)
        if index > indexmax: indexmax = index
        cwnd[index].append(float(value[VINDEX]))
xstep = STEP / 2
for i in range(indexmax + 1):
    x1.append(xstep)
    xstep += STEP
    y1.append(mean(cwnd[i]))

file21 = '/root/ndn/proj-sep/log/multiport/ecp-c0.log'
file22 = '/root/ndn/proj-sep/log/multiport/ecp-c1.log'
file23 = '/root/ndn/proj-sep/log/multiport/ecp-c2.log'
x2, y2 = [], []
ecpc0 = open(file21, 'r').readlines()
ecpc1 = open(file22, 'r').readlines()
ecpc2 = open(file23, 'r').readlines()
ecps = ecpc1
cwnd = [[] for _ in range(1000)]
indexmax = 0
for line in ecps:
    value = line.replace(' ', '').split(',')
    if (len(value) >= 3 and value[2] == 'data'):
        index = int(float(value[1]) / STEP)
        if index > indexmax: indexmax = index
        cwnd[index].append(float(value[VINDEX]))
xstep = STEP / 2
for i in range(indexmax + 1):
    x2.append(xstep)
    xstep += STEP
    y2.append(mean(cwnd[i]))

file31 = '/root/ndn/proj-sep/log/multiport/dqn-c0.log'
file32 = '/root/ndn/proj-sep/log/multiport/dqn-c1.log'
file33 = '/root/ndn/proj-sep/log/multiport/dqn-c2.log'
x3, y3 = [], []
dqnc0 = open(file31, 'r').readlines()
dqnc1 = open(file32, 'r').readlines()
dqnc2 = open(file33, 'r').readlines()
dqns = dqnc1
cwnd = [[] for _ in range(1000)]
indexmax = 0
for line in dqns:
    value = line.replace(' ', '').split(',')
    if (len(value) >= 3 and value[2] == 'data'):
        index = int(float(value[1]) / STEP)
        if index > indexmax: indexmax = index
        cwnd[index].append(float(value[VINDEX]))
xstep = STEP / 2
for i in range(indexmax + 1):
    x3.append(xstep)
    y3.append(mean(cwnd[i]))
    xstep += STEP

file41 = '/root/ndn/proj-sep/log/multiport/ddpg-c0.log'
file42 = '/root/ndn/proj-sep/log/multiport/ddpg-c1.log'
file43 = '/root/ndn/proj-sep/log/multiport/ddpg-c2.log'
x4, y4 = [], []
ddpgc0 = open(file41, 'r').readlines()
ddpgc1 = open(file42, 'r').readlines()
ddpgc2 = open(file43, 'r').readlines()
ddpgs = ddpgc1 + ddpgc2
cwnd = [[] for _ in range(1000)]
indexmax = 0
for line in ddpgs:
    value = line.replace(' ', '').split(',')
    if (len(value) >= 3 and value[2] == 'data'):
        index = int(float(value[1]) / STEP)
        if index > indexmax: indexmax = index
        cwnd[index].append(float(value[VINDEX]))
xstep = STEP / 2
for i in range(indexmax + 1):
    x4.append(xstep)
    y4.append(mean(cwnd[i]))
    xstep += STEP

#plt.plot([Y_1,Y_2,Y_3])
#fig,ax = plt.subplots()
#x = np.linespace(0,200,100)
#x = np.linspace(0, 50, 50)

plt.figure(figsize=(9.0, 4.5))

f1, = plt.plot(x1, y1, color='red', label='ICP', ls='-.')
f2, = plt.plot(x2, y2, color='#1A6FDF', label='ECP', ls=':')
f3, = plt.plot(x3, y3, color='#37AD6B', label='DRL-CCP', ls='dashed')  #B177DE
f4, = plt.plot(x4, y4, color='#CC9900', label='IEACC', ls='dotted')
#f5, = plt.plot(xxx, yyy, color='slategrey', label='Bandwidth', ls='-')
#ax.plot(y1,color='black',linestyle='-')

plt.legend(handles=[f1, f2, f3, f4],
           labels=['ICP', 'ECP', 'DRL-CCP', 'IEACC'],
           loc='lower right')
#plt.ylim((3,10))
#ax.legend()
#plt.grid(axis="y")

plt.grid(axis="y", linestyle='-.')
plt.xlabel("time (s)")
plt.ylabel("cwnd")

#plt.xlim((0,6000))
plt.savefig('./cwnd.png')
#plt.show()