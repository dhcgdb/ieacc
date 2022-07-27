#import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
num_old =0
filename = '/root/ndnproj-0707/ndnproj/results/data/50s_ECP_retrans_100.txt'
#X,Y = [],[]
datamax =0 
ofonum=0
with open(filename, 'r') as f:
    lines = f.readlines()[7:]
    for line in lines:
        value = [s for s in line.split(",")]
        #print(len(value))
        if(len(value)==4):
            num_new = float(value[1])
            if (num_old !=(num_new-1) ):
                print('old_num:',num_old,'new_num:',float(value[1]))  
                ofonum= ofonum+1
            num_old = num_new            
            Y=float(value[1])
            X=float(value[3])
        if(len(value)==16):
            data = float(value[9])
            if(datamax<data):
                datamax =data
            #break
print('interestcout:',X,'interestsendcur: ',Y,'datareceived:',datamax,'totoalofonum: ',ofonum)
#plt.boxplot(Y)
#plt.grid(axis="y")
#plt.grid(axis="y",linestyle='-.')


#plt.xlim((0,6000))
#plt.savefig('./rtt_DDPG.jpg')
#plt.show()