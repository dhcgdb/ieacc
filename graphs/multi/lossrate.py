#import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

filename_1 = '/root/ndnproj-0707/ndnproj/results/data/loss_AIMD_80.txt'
filename_2 = '/root/ndnproj-0707/ndnproj/results/data/loss_AIMD_retrans_80.txt'
filename_3 = '/root/ndnproj-0707/ndnproj/results/data/loss_ECP_80.txt'
filename_4 = '/root/ndnproj-0707/ndnproj/results/data/loss_ECP_retrans_80.txt'
filename_5 = '/root/ndnproj-0707/ndnproj/results/data/loss_DDPG_80.txt'
X,Y_1,Y_2 = [],[],[]
Y_3,Y_4,Y_5 =[],[],[]
t =0
Y_11,Y_12,Y_13,Y_14,Y_15=[],[],[],[],[]
step=5.0
ofonum =0 
step1=step
packet =1024
num_old=0
with open(filename_1, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            t = float(value[1])
            if(t <step1):
                data = float(value[9])
                if(num_old!=(data-1)):
                    ofonum =ofonum+1
                num_old =data
            else:    
                a =float(ofonum*packet*8)/(step*1000)   
                b=ofonum         
                Y_1.append(a)
                Y_11.append(b)
                step1=step1+step
                X.append(t)
                ofonum=0
ofonum=0
numold=0
t=0
step1 =step
with open(filename_2, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            t = float(value[1])
            if(t <step1):
                data = float(value[9])
                if(num_old!=(data-1)):
                    ofonum =ofonum+1
                num_old =data
            else:    
                a =float(ofonum*packet*8)/(step*1000)   
                b=ofonum         
                Y_2.append(a)
                Y_12.append(b)
                step1=step1+step
                ofonum=0
                
ofonum=0
numold=0
t=0
step1 =step
with open(filename_3, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            t = float(value[1])
            if(t <step1):
                data = float(value[9])
                if(num_old!=(data-1)):
                    ofonum =ofonum+1
                num_old =data
            else:    
                a =float(ofonum*packet*8)/(step*1000)   
                b=ofonum         
                Y_3.append(a)
                Y_13.append(b)
                step1=step1+step
                ofonum=0
ofonum=0
numold=0
t=0
step1 =step
with open(filename_4, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            t = float(value[1])
            if(t <step1):
                data = float(value[9])
                if(num_old!=(data-1)):
                    ofonum =ofonum+1
                num_old =data
            else:    
                a =float(ofonum*packet*8)/(step*1000)   
                b=ofonum         
                Y_4.append(a)
                Y_14.append(b)
                step1=step1+step
                ofonum=0
ofonum=0
numold=0
t=0
step1 =step
with open(filename_5, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==16):
            t = float(value[1])
            if(t <step1):
                data = float(value[9])
                if(num_old!=(data-1)):
                    ofonum =ofonum+1
                num_old =data
            else:    
                a =float(ofonum*packet*8)/(step*1000)   
                b=ofonum         
                Y_5.append(a)
                Y_15.append(b)
                step1=step1+step
                ofonum=0

#plt.plot([Y_1,Y_2,Y_3])
#fig,ax = plt.subplots()
#x = np.linespace(0,200,100)
x=np.linspace(0,50,50)
y1=73.7
m=399
X=X[0:m]
print(len(Y_1),len(Y_2),len(Y_3),len(Y_4),len(Y_5))
f1,=plt.plot(X,Y_1[0:m],color='#1A6FDF',label='AIMD',marker='+',ls='',markersize=5)
f2,=plt.plot(X,Y_2[0:m],color='#37AD6B',label='AIMD_a',marker='*',ls='',markersize=5)
f3,=plt.plot(X,Y_3[0:m],color='#B177DE',label='ECP',marker='D',ls='',markersize=5)
f4,=plt.plot(X,Y_4[0:m],color='#CC9900',label='ECP_a',marker='o',ls='',markersize=5)
f5,=plt.plot(X,Y_5[0:m],color='red',label='IEACC',marker='x',ls='',markersize=5)
#ax.plot(y1,color='black',linestyle='-')

plt.legend(handles =[f1,f2,f3,f4,f5],labels=['AIMD','AIMD_a','ECP','ECP_a','IEACC'],loc='upper left')
plt.ylim((0,50))
#ax.legend()
#plt.grid(axis="y")
plt.grid(axis="y",linestyle='-.')
plt.xlabel("time (s)")
plt.ylabel("Packet drop rate (Kbps)")

#plt.xlim((0,6000))
plt.savefig('./useful_lr_1.jpg')
#plt.show()