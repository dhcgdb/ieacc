#import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
filename_1 = '/root/ndnproj-0707/ndnproj/results/newdata/30s-AIMD-60bf.txt'
filename_2 = '/root/ndnproj-0707/ndnproj/results/newdata/30s-AIMD-80bf.txt'
filename_3 = '/root/ndnproj-0707/ndnproj/results/newdata/30s-AIMD-100bf.txt'
filename_4 = '/root/ndnproj-0707/ndnproj/results/newdata/30s-ECP-60bf.txt'
filename_5 = '/root/ndnproj-0707/ndnproj/results/newdata/30s-ECP-80bf.txt'
filename_6 = '/root/ndnproj-0707/ndnproj/results/newdata/30s-ECP-100bf.txt'
filename_7 = '/root/ndnproj-0707/ndnproj/results/newdata/30s-ECP-retrans1-60bf.txt'
filename_8 = '/root/ndnproj-0707/ndnproj/results/newdata/30s-ECP-retrans1-80bf.txt'
filename_9 = '/root/ndnproj-0707/ndnproj/results/newdata/30s-ECP-retrans1-100bf.txt'

filename_11 = '/root/ndnproj-0707/ndnproj/results/newdata/30s-AIMD-retrans-60bf.txt'
filename_12 = '/root/ndnproj-0707/ndnproj/results/newdata/30s-AIMD-retrans-80bf.txt'
filename_13 = '/root/ndnproj-0707/ndnproj/results/newdata/30s-AIMD-retrans-100bf.txt'
filename_14 = '/root/ndnproj-0707/ndnproj/results/newdata/30s-ECP-retrans-60bf.txt'
filename_15 = '/root/ndnproj-0707/ndnproj/results/newdata/30s-ECP-retrans-80bf.txt'
filename_16 = '/root/ndnproj-0707/ndnproj/results/newdata/30s-ECP-retrans-100bf.txt'

X,Y_1,Y_2,Y_3 = [],[],[],[]
Y_4,Y_5,Y_6 =[],[],[]
Y_7,Y_8,Y_9 =[],[],[]
Y_11,Y_12,Y_13 = [],[],[]
Y_14,Y_15,Y_16 =[],[],[]

num=0
n=30
a=[]
station =13
with open(filename_1, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            if(num <n):
                a.append(float(value[station])*1000)
                num = num+1
            else:
                Y_1.append(np.mean(a))
                num=0
                a.clear()
                X.append(float(value[station]))
            data = value[9]
            #break
num=0
a.clear()
print("AIMD_60----total_data_transmited: ",data)
with open(filename_11, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            if(num <n+20):
                a.append(float(value[station])*1000)
                num = num+1
            else:
                Y_11.append(np.mean(a))
                num=0
                a.clear()
                X.append(float(value[1]))
            data = value[9]
            #break
print("AIMD_retrans_60----total_data_transmited: ",data)
num=0
a.clear()
with open(filename_4, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            if(num <n):
                a.append(float(value[station])*1000)
                num = num+1
            else:
                Y_4.append(np.mean(a))
                num=0
                a.clear()
                X.append(float(value[1]))
            data = value[9]
print("ECP_60---- total_data_transmited: ",data)
num=0
a.clear()
with open(filename_14, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            if(num <n):
                a.append(float(value[station])*1000)
                num = num+1
            else:
                Y_14.append(np.mean(a))
                num=0
                a.clear()
                X.append(float(value[1]))
            data = value[9]
print("ECP_retrans_60---- total_data_transmited: ",data)
num=0
a.clear()
with open(filename_7, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            if(num <n):
                a.append(float(value[station])*1000)
                num = num+1
            else:
                Y_7.append(np.mean(a))
                num=0
                a.clear()
                X.append(float(value[1]))
            data = value[9]
print("DDPG_60---- total_data_transmited: ",data)
num=0
a.clear()

with open(filename_2, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            if(num <n):
                a.append(float(value[station])*1000)
                num = num+1
            else:
                Y_2.append(np.mean(a))
                num=0
                a.clear()
                X.append(float(value[1]))
            data = value[9]
print("AIMD_80---- total_data_transmited: ",data)
num=0
a.clear()
with open(filename_12, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            if(num <n):
                a.append(float(value[station])*1000)
                num = num+1
            else:
                Y_12.append(np.mean(a))
                num=0
                a.clear()
                X.append(float(value[1]))
            data = value[9]
print("AIMD_retrans_80---- total_data_transmited: ",data)
num=0
a.clear()
with open(filename_5, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            if(num <n):
                a.append(float(value[station])*1000)
                num = num+1
            else:
                Y_5.append(np.mean(a))
                num=0
                a.clear()
                X.append(float(value[1]))
            data = value[9]
print("ECP_80---- total_data_transmited: ",data)
num=0
a.clear()

with open(filename_15, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            if(num <n):
                a.append(float(value[station])*1000)
                num = num+1
            else:
                Y_15.append(np.mean(a))
                num=0
                a.clear()
                X.append(float(value[1]))
            data = value[9]
print("ECP_retrans_80---- total_data_transmited: ",data)
num=0
a.clear()
with open(filename_8, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            if(num <n):
                a.append(float(value[station])*1000)
                num = num+1
            else:
                Y_8.append(np.mean(a))
                num=0
                a.clear()
                X.append(float(value[1]))
            data = value[9]
print("DDPG_80---- total_data_transmited: ",data)
num=0
a.clear()

with open(filename_3, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            if(num <n):
                a.append(float(value[station])*1000)
                num = num+1
            else:
                Y_3.append(np.mean(a))
                num=0
                a.clear()
                X.append(float(value[1]))
            data = value[9]
print("AIMD_100---- total_data_transmited: ",data)
num=0
a.clear()
with open(filename_13, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            if(num <n):
                a.append(float(value[station])*1000)
                num = num+1
            else:
                Y_13.append(np.mean(a))
                num=0
                a.clear()
                X.append(float(value[1]))
            data = value[9]
print("AIMD_retrans_100---- total_data_transmited: ",data)
num=0
a.clear()
with open(filename_6, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            if(num <n):
                a.append(float(value[station])*1000)
                num = num+1
            else:
                Y_6.append(np.mean(a))
                num=0
                a.clear()
                X.append(float(value[1]))
            data = value[9]
print("ECP_100---- total_data_transmited: ",data)
num=0
a.clear()
with open(filename_16, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            if(num <n):
                a.append(float(value[station])*1000)
                num = num+1
            else:
                Y_16.append(np.mean(a))
                num=0
                a.clear()
                X.append(float(value[1]))
            data = value[9]
print("ECP_retrans_100---- total_data_transmited: ",data)
num=0
a.clear()
with open(filename_9, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            if(num <n):
                a.append(float(value[station])*1000)
                num = num+1
            else:
                Y_9.append(np.mean(a))
                num=0
                a.clear()
                X.append(float(value[1]))
            data = value[9]
print("DDPG_100---- total_data_transmited: ",data)
num=0
a.clear()

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

plt.figure(figsize=(5,4.0))
fig=sns.boxplot(x="Threshold", y="Delay (ms)", data=data, hue="algorithms", width=0.6, linewidth=1.0, palette="Set2",saturation=0.5,showfliers=True,fliersize=4.0,medianprops={'linestyle':'-','color':'black'},whiskerprops = {'linestyle':'-.'},showmeans=False,meanprops={'marker':'D','color':'blue'}) 
fig.legend(loc='upper center',bbox_to_anchor=(0.25,0.9999))

#plt.ylim((40,250))
#plt.xlim((50,110))
#params = {'figure.figsize':'6,5'}
#plt.rcParams.update(params)
plt.grid(axis="y",linestyle='-.')
plt.savefig('./test_rtt_6.jpg')

