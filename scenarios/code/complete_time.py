#import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

filename_1 = '/root/ndnproj-0707/ndnproj/results/data/200s_ECP_60.txt'
filename_2 = '/root/ndnproj-0707/ndnproj/results/data/200s_ECP.txt'
filename_3 = '/root/ndnproj-0707/ndnproj/results/data/ECP_100.txt'
filename_4 = '/root/ndnproj-0707/ndnproj/results/data/200s_ECP_retrans_60.txt'
filename_5 = '/root/ndnproj-0707/ndnproj/results/data/200s_ECP_retrans.txt'
filename_6 = '/root/ndnproj-0707/ndnproj/results/data/200s_ECP_retrans_100.txt'
filename_7 = '/root/ndnproj-0707/ndnproj/results/data/200s_DDPG_retrans.txt'


X,Y_1,Y_2,Y_3,Y_4,Y_5,Y_6,Y_7 = [],[],[],[],[],[],[],[]
X=[5000,10000,30000]
W =[]
with open(filename_1, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            if(float(value[9])==float(X[0])):
                Y_1.append(float(value[1]))
            if(float(value[9])==float(X[1])):
                Y_1.append(float(value[1]))
            if(float(value[9])==float(X[2])):
                Y_1.append(float(value[1]))
            W.append(float(value[5]))
            data = value[9]
print('AIMD_pure: totoal data--',data, 'average window: ',np.mean(W),'10000: ',Y_1[0],' 30000: ',Y_1[1], ' 50000: ',Y_1[2], )
W.clear()
with open(filename_2, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            if(float(value[9])==float(X[0])):
                Y_2.append(float(value[1]))
            if(float(value[9])==float(X[1])):
                Y_2.append(float(value[1]))
            if(float(value[9])==float(X[2])):
                Y_2.append(float(value[1]))
            data = value[9]
            W.append(float(value[5]))
print('AIMD_nack: totoal data---',data,' average window: ',np.mean(W),'10000: ',Y_2[0],' 30000: ',Y_2[1], ' 50000: ',Y_2[2])
W.clear()
with open(filename_3, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            if(float(value[9])==float(X[0])):
                Y_3.append(float(value[1]))
            if(float(value[9])==float(X[1])):
                Y_3.append(float(value[1]))
            if(float(value[9])==float(X[2])):
                Y_3.append(float(value[1]))
            data = value[9]
            W.append(float(value[5]))
print('AIMD_retrans: totoal data--',data,' average window: ',np.mean(W),'10000: ',Y_3[0],' 30000: ',Y_3[1], ' 50000: ',Y_3[2])
W.clear()
with open(filename_4, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            if(float(value[9])==float(X[0])):
                Y_4.append(float(value[1]))
            if(float(value[9])==float(X[1])):
                Y_4.append(float(value[1]))
            if(float(value[9])==float(X[2])):
                Y_4.append(float(value[1]))
            data = value[9]
            W.append(float(value[5]))
print('ECP_pure: --totaol data ',data,' average window: ',np.mean(W),'10000: ',Y_4[0],' 30000: ',Y_4[1], ' 50000: ',Y_4[2])
W.clear()
with open(filename_5, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            if(float(value[9])==float(X[0])):
                Y_5.append(float(value[1]))
            if(float(value[9])==float(X[1])):
                Y_5.append(float(value[1]))
            if(float(value[9])==float(X[2])):
                Y_5.append(float(value[1]))
            data = value[9]
            W.append(float(value[5]))
print('ECP_retrans: totoal data---',data,' average window: ',np.mean(W),'10000: ',Y_5[0],' 30000: ',Y_5[1], ' 50000: ',Y_5[2])
W.clear()
with open(filename_6, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            if(float(value[9])==float(X[0])):
                Y_6.append(float(value[1]))
            if(float(value[9])==float(X[1])):
                Y_6.append(float(value[1]))
            if(float(value[9])==float(X[2])):
                Y_6.append(float(value[1]))
            data = value[9]
            W.append(float(value[5]))
print('DDPG_pure: totoal data--',data,' average window: ',np.mean(W),'10000: ',Y_6[0],' 30000: ',Y_6[1], ' 50000: ',Y_6[2])
W.clear()
with open(filename_7, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            if(float(value[9])==float(X[0])):
                Y_7.append(float(value[1]))
            if(float(value[9])==float(X[1])):
                Y_7.append(float(value[1]))
            if(float(value[9])==float(X[2])):
                Y_7.append(float(value[1]))
            data = value[9]
            W.append(float(value[5]))
print('DDPG_retrans: totoal data--',data,' average window: ',np.mean(W),'10000: ',Y_7[0],' 30000: ',Y_7[1], ' 50000: ',Y_7[2])
W.clear()
#labels ='AIMD_r','ECP_r','IEACC',' ','AIMD_r','ECP_r','IEACC',' ','AIMD_r','ECP_r','IEACC'


#plt.boxplot([Y_1,Y_4,Y_7,X,Y_2,Y_5,Y_8,X,Y_3,Y_6,Y_9], showfliers=False, labels = labels, showmeans = True,whiskerprops = {'linestyle':'-.'})#flierprops={'marker':'o','color':'black'}
#plt.grid(axis="y")
#plt.grid(axis="y",linestyle='-.')


#plt.xlim((0,6000))
#plt.xticks(rotation=60)
#plt.xticks(fontsize=9)
#plt.savefig('./rtt_buffer.jpg')
#plt.show()