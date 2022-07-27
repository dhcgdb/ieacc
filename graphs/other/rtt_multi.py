#import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
filename_1 = '/root/ndnproj-0707/ndnproj/results/data/AIMD_60.txt'
filename_2 = '/root/ndnproj-0707/ndnproj/results/data/loss_AIMD_80.txt'
filename_3 = '/root/ndnproj-0707/ndnproj/results/data/AIMD_100.txt'
filename_4 = '/root/ndnproj-0707/ndnproj/results/data/ECP_60.txt'
filename_5 = '/root/ndnproj-0707/ndnproj/results/data/loss_ECP_80_.txt'
filename_6 = '/root/ndnproj-0707/ndnproj/results/data/ECP_100_.txt'
filename_7 = '/root/ndnproj-0707/ndnproj/results/data/DDPG_retrans_60.txt'
filename_8 = '/root/ndnproj-0707/ndnproj/results/data/DDPG_retrans_80.txt'
filename_9 = '/root/ndnproj-0707/ndnproj/results/data/DDPG_retrans_100.txt'

filename_11 = '/root/ndnproj-0707/ndnproj/results/data/AIMD_retrans_60.txt'
filename_12 = '/root/ndnproj-0707/ndnproj/results/data/loss_AIMD_retrans_80.txt'
filename_13 = '/root/ndnproj-0707/ndnproj/results/data/AIMD_retrans_100.txt'
filename_14 = '/root/ndnproj-0707/ndnproj/results/data/ECP_retrans_60.txt'
filename_15 = '/root/ndnproj-0707/ndnproj/results/data/loss_ECP_retrans_80_.txt'
filename_16 = '/root/ndnproj-0707/ndnproj/results/data/ECP_retrans_100.txt'

X,Y_1,Y_2,Y_3 = [],[],[],[]
Y_4,Y_5,Y_6 =[],[],[]
Y_7,Y_8,Y_9 =[],[],[]
Y_11,Y_12,Y_13 = [],[],[]
Y_14,Y_15,Y_16 =[],[],[]

with open(filename_1, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            Y_1.append(float(value[13])*100)
            data = value[9]
            #break
print("AIMD_60----total_data_transmited: ",data)
with open(filename_11, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            Y_11.append(float(value[13])*100)
            data = value[9]
            #break
print("AIMD_retrans_60----total_data_transmited: ",data)
with open(filename_4, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            Y_4.append(float(value[13])*100)
            data = value[9]
print("ECP_60---- total_data_transmited: ",data)
with open(filename_14, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            Y_14.append(float(value[13])*100)
            data = value[9]
print("ECP_retrans_60---- total_data_transmited: ",data)
with open(filename_7, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            Y_7.append(float(value[13])*100)
            data = value[9]
print("DDPG_60---- total_data_transmited: ",data)

with open(filename_2, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            Y_2.append(float(value[13])*100)
            data = value[9]
print("AIMD_80---- total_data_transmited: ",data)
with open(filename_12, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            Y_12.append(float(value[13])*100)
            data = value[9]
print("AIMD_retrans_80---- total_data_transmited: ",data)
with open(filename_5, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            Y_5.append(float(value[13])*100)
            data = value[9]
print("ECP_80---- total_data_transmited: ",data)

with open(filename_15, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            Y_15.append(float(value[13])*100)
            data = value[9]
print("ECP_retrans_80---- total_data_transmited: ",data)
with open(filename_8, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            Y_8.append(float(value[13])*100)
            data = value[9]
print("DDPG_80---- total_data_transmited: ",data)

with open(filename_3, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            Y_3.append(float(value[13])*100)
            data = value[9]
print("AIMD_100---- total_data_transmited: ",data)
with open(filename_13, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            Y_13.append(float(value[13])*100)
            data = value[9]
print("AIMD_retrans_100---- total_data_transmited: ",data)
with open(filename_6, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            Y_6.append(float(value[13])*100)
            data = value[9]
print("ECP_100---- total_data_transmited: ",data)
with open(filename_16, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            Y_16.append(float(value[13])*100)
            data = value[9]
print("ECP_retrans_100---- total_data_transmited: ",data)
with open(filename_9, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            Y_9.append(float(value[13])*100)
            data = value[9]
print("DDPG_100---- total_data_transmited: ",data)

print(Y_1[1:10])
print(type(Y_1))
#labels ='AIMD_a','ECP_a','IEACC',' ','AIMD_a','ECP_a','IEACC',' ','AIMD_a','ECP_a','IEACC'


#fig1=plt.boxplot([Y_1,Y_11,Y_4,Y_14,Y_7,X,Y_2,Y_12,Y_5,Y_15,Y_8,X,Y_3,Y_13,Y_6,Y_16,Y_9], showfliers=False, showmeans = True,whiskerprops = {'linestyle':'-.'})#flierprops={'marker':'o','color':'black'}
#plt.grid(axis="y")
#colors=['pink','lightblue','lightgreen','lightcoral','mediumslateblue','black','pink','lightblue','lightgreen','lightcoral','mediumslateblue','black','pink','lightblue','lightgreen','lightcoral','mediumslateblue']
#plt.grid(axis="y",linestyle='-.')
#for bplot in fig1:
#    for patch,color in zip(bplot['boxes'],colors):
#        patch.set_facecolor(color)

y_60=list(Y_1+Y_11+Y_4+Y_14+Y_7)
y_80=list(Y_2+Y_12+Y_5+Y_15+Y_8)
y_100=list(Y_3+Y_13+Y_6+Y_16+Y_9)
y_60=[y_60,list(['60']*len(y_60))]
y_80=[y_80,list(['80']*len(y_80))]
y_100=[y_100,list(['100']*len(y_100))]
y_60=[y_60[0],y_60[1],list(['AIMD']*len(Y_1)+['AIMD_a']*len(Y_11)+['ECP']*len(Y_4)+['ECP_a']*len(Y_14)+['IEACC']*len(Y_7))]
y_80=[y_80[0],y_80[1],list(['AIMD']*len(Y_2)+['AIMD_a']*len(Y_12)+['ECP']*len(Y_5)+['ECP_a']*len(Y_15)+['IEACC']*len(Y_8))]
y_100=[y_100[0],y_100[1],list(['AIMD']*len(Y_3)+['AIMD_a']*len(Y_13)+['ECP']*len(Y_6)+['ECP_a']*len(Y_16)+['IEACC']*len(Y_9))]

print(len(y_60[0]))
print(len(y_60[1]))
print(len(y_60[2]))
y=list(y_60[0]+y_80[0]+y_100[0])
x=list(y_60[1]+y_80[1]+y_100[1])
group=list(y_60[2]+y_80[2]+y_100[2])
from pandas.core.frame import DataFrame
data={"Threshold" : x,
    "algorithms": group,
   "Delay (ms)" : y}#将列表a，b转换成字典
data=DataFrame(data)#将字典转换成为数据框

import seaborn as sns 
import matplotlib.pyplot as plt 


fig=sns.boxplot(x="Threshold", y="Delay (ms)", data=data, hue="algorithms", width=0.5, linewidth=1.0, palette="Set3",showfliers=False,medianprops={'linestyle':'-','color':'black'},whiskerprops = {'linestyle':'-.'},showmeans=False,meanprops={'marker':'D','color':'blue'}) 
fig.legend(loc='lower left',bbox_to_anchor=(0.25,0.9999))
plt.ylim((4,10))
plt.grid(axis="y",linestyle='-.')
plt.savefig('./useful_rtt_1.jpg')

