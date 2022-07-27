STEP = 0.5
PACKET = 1024
VINDEX = 0

file11 = '/root/ndn/proj-sep/log/multiport/ecp-c0.log'
file12 = '/root/ndn/proj-sep/log/multiport/ecp-c1.log'
x1, y1 = [], []
dqns = open(file11, 'r').readlines() + open(file12, 'r').readlines()
datanum = [0] * 1000
indexmax = 0
for line in dqns:
    value = line.replace(' ', '').split(',')
    if (len(value) >= 3 and value[2] == 'data'):
        index = int(float(value[1]) / STEP)
        if index > indexmax: indexmax = index
        datanum[index] += 1
xstep = STEP / 2
for i in range(indexmax + 1):
    x1.append(xstep)
    xstep += STEP
    y1.append(float(datanum[i] * PACKET * 8) / (STEP * 1000 * 1000))


file21 = '/root/ndn/proj-sep/log/multiport/ecpbn-c0.log'
file22 = '/root/ndn/proj-sep/log/multiport/ecpbn-c1.log'
x2, y2 = [], []
dqnbns = open(file21, 'r').readlines() + open(file22, 'r').readlines()
datanum = [0] * 1000
indexmax = 0
for line in dqnbns:
    value = line.replace(' ', '').split(',')
    if (len(value) >= 3 and value[2] == 'data'):
        index = int(float(value[1]) / STEP)
        if index > indexmax: indexmax = index
        datanum[index] += 1
xstep = STEP / 2
for i in range(indexmax + 1):
    x2.append(xstep)
    xstep += STEP
    y2.append(float(datanum[i] * PACKET * 8) / (STEP * 1000 * 1000))


file31 = '/root/ndn/proj-sep/log/multiport/ecpbn1-c0.log'
file32 = '/root/ndn/proj-sep/log/multiport/ecpbn1-c1.log'
x3, y3 = [], []
ddpgbns = open(file31, 'r').readlines() \
     + open(file32, 'r').readlines()
datanum = [0] * 1000
indexmax = 0
for line in ddpgbns:
    value = line.replace(' ', '').split(',')
    if (len(value) >= 3 and value[2] == 'data'):
        index = int(float(value[1]) / STEP)
        if index > indexmax: indexmax = index
        datanum[index] += 1
xstep = STEP / 2
for i in range(indexmax + 1):
    x3.append(xstep)
    y3.append(float(datanum[i] * PACKET * 8) / (STEP * 1000 * 1000))
    xstep += STEP
#
#file41 = '/root/ndn/proj-sep/log/multiport/ddpg-c0.log'
#file42 = '/root/ndn/proj-sep/log/multiport/ddpg-c1.log'
#file43 = '/root/ndn/proj-sep/log/multiport/ddpg-c2.log'
#x4, y4 = [], []
#ddpgs = open(file41, 'r').readlines() \
#      + open(file42, 'r').readlines() \
#      + open(file43, 'r').readlines()
#datanum = [0] * 1000
#indexmax = 0
#for line in ddpgs:
#    value = line.replace(' ', '').split(',')
#    if (len(value) >= 3 and value[2] == 'data'):
#        index = int(float(value[1]) / STEP)
#        if index > indexmax: indexmax = index
#        datanum[index] += 1
#xstep = STEP / 2
#for i in range(indexmax + 1):
#    x4.append(xstep)
#    y4.append(float(datanum[i] * PACKET * 8) / (STEP * 1000 * 1000))
#    xstep += STEP
#
#
#file51 = '/root/ndn/proj-sep/log/multiport/dqnbn1-c0.log'
#file52 = '/root/ndn/proj-sep/log/multiport/dqnbn1-c1.log'
#x5, y5 = [], []
#ddpgbn2s = open(file51, 'r').readlines() \
#     + open(file52, 'r').readlines()
#datanum = [0] * 1000
#indexmax = 0
#for line in ddpgbn2s:
#    value = line.replace(' ', '').split(',')
#    if (len(value) >= 3 and value[2] == 'data'):
#        index = int(float(value[1]) / STEP)
#        if index > indexmax: indexmax = index
#        datanum[index] += 1
#xstep = STEP / 2
#for i in range(indexmax + 1):
#    x5.append(xstep)
#    y5.append(float(datanum[i] * PACKET * 8) / (STEP * 1000 * 1000))
#    xstep += STEP
#
#file61 = '/root/ndn/proj-sep/log/multiport/ecpbn-c0.log'
#file62 = '/root/ndn/proj-sep/log/multiport/ecpbn-c1.log'
#x5, y5 = [], []
#ddpgbn2s = open(file51, 'r').readlines() \
#     + open(file52, 'r').readlines()
#datanum = [0] * 1000
#indexmax = 0
#for line in ddpgbn2s:
#    value = line.replace(' ', '').split(',')
#    if (len(value) >= 3 and value[2] == 'data'):
#        index = int(float(value[1]) / STEP)
#        if index > indexmax: indexmax = index
#        datanum[index] += 1
#xstep = STEP / 2
#for i in range(indexmax + 1):
#    x5.append(xstep)
#    y5.append(float(datanum[i] * PACKET * 8) / (STEP * 1000 * 1000))
#    xstep += STEP


import matplotlib
matplotlib.use('cairo')
import matplotlib.pyplot as plt
#plt.plot([Y_1,Y_2,Y_3])
#fig,ax = plt.subplots()
#x = np.linespace(0,200,100)
#x = np.linspace(0, 50, 50)

plt.figure(figsize=(9.0, 4.5))

f1, = plt.plot(x1, y1, color='red', label='ecp', ls='-.')
f2, = plt.plot(x2, y2, color='#1A6FDF', label='ecpBN', ls=':')
f3, = plt.plot(x3, y3, color='#37AD6B', label='ecpBN-W', ls='dashed')  #B177DE
#f4, = plt.plot(x4, y4, color='#CC9900', label='DDPGBN-W', ls='dotted')
#f5, = plt.plot(x5, y5, color='purple', label='DQNBN', ls='--')
#f5, = plt.plot(xxx, yyy, color='slategrey', label='Bandwidth', ls='-')
#ax.plot(y1,color='black',linestyle='-')

plt.legend(handles=[f1,f2,f3],
           labels=['ecp','ecpBN','ecpBN-W'],
           loc='lower right')
#plt.ylim((3,10))
#ax.legend()
#plt.grid(axis="y")

plt.grid(axis="y", linestyle='-.')
plt.xlabel("time (s)")
plt.ylabel("Data transmission rate (Mbps)")

#plt.xlim((0,6000))
plt.savefig('./comp1.png')
#plt.show()