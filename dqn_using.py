import math
from os import makedirs, path, write
import os
from numpy.random import gamma
from py_interface import *
from ctypes import *
import torch
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
#import matplotlib.pyplot as plt
import time

from torch.nn.modules import loss


class NdnParam(Structure):
    _pack_ = 1
    _fields_ = [
        ('cWnd', c_double),
        ('avgDelay', c_double),
        ('Data', c_uint32),
        ('InFlight', c_uint32),
        ('Nloss', c_uint32),
        ('Rloss', c_uint32),
        ('Ninter', c_uint32),
        ('Nretrans', c_uint32),
    ]


class RetScale(Structure):
    _pack_ = 1
    _fields_ = [('newCwnd', c_double)]


MAX_EPISODES = 500
MAX_EP_STEPS = 200
LR = 0.01  # learning rate 
GAMMA = 0.9  # reward discount
MEMORY_CAPACITY = 50
BATCH_SIZE = 32

epsilon = 0.1
#Reset()


class Net(nn.Module):
    def __init__(self, s_dim, a_dim):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(s_dim, 30)
        self.fc1.weight.data.normal_(0, 0.1)
        self.out = nn.Linear(30, a_dim)
        self.out.weight.data.normal_(0, 0.1)

    def forward(self, x):
        x = self.fc1(x)
        x = F.relu(x)
        x = self.out(x)
        x = 4 * F.tanh(x) + 4
        #x = torch.tanh(x)
        #actions_value = x
        return x

class DQN(object):
    def __init__(self):
        self.eval_net = torch.load("results/dqn_model_3/188/eval_net.model")
        self.target_net = torch.load("results/dqn_model_3/188/target_net.model")

    def choose_action(self, s):
        s = torch.unsqueeze(torch.FloatTensor(s), 0)
        return self.eval_net(s)[0].detach()

def ndngetstate(var):
    data = var.Acquire()
    cWnd = data.env.cWnd
    delay = data.env.avgDelay
    acks = data.env.Data
    inflight = data.env.InFlight
    Rloss = data.env.Rloss
    Ninter = data.env.Ninter
    var.ReleaseAndRollback()
    print('cWnd:',cWnd,',acks:',acks,',delay:',delay,',Rloss:',Rloss,',Ninter:',Ninter)
    #acks = acks / 700
    #delay = (0.13 - delay) / 0.11
    #return [cWnd/301.0,float(acks)/200.0, delay,float(Rloss)/5.0,float(Ninter)/100.0]
    return [cWnd/601.0,float(acks)/350.0, delay,float(Rloss)/20.0]


def ndnstep(a, var):
    data = var.Acquire()
    data.act.newCwnd = c_double(a)#c_double(a).value
    var.Release()
    s = ndngetstate(var)

    r = s[0]+s[1]-10*s[2]-s[3]*1.9 #r = s[0]+s[1]-10*s[2]-s[3]#-float(s[3])/32.0
    #print('float(s[1])/(s[2]+0.00011):',float(s[1])/(s[2]+1),'float(s[3])/32.0:',float(s[3])/32.0)
    #if(s[3]>=79):
    #    r =-200
    #if(r>200):
    #    r =200
    #if(r<-200):
    #    r = -200
    return s, r

def ndnreset(exp, var):
    exp.reset()                       
    exp.run(None, True)
    return ndngetstate(var)


#actiontype = "random"
dqn = DQN()
FreeMemory()
exp = Experiment(1234, 2120, "1c1p", "./")
var = Ns3AIRL(1024, NdnParam, RetScale)

j=0
s = ndnreset(exp, var)
while(True):
    act = np.double(dqn.choose_action(s))
    print('act:',act)
    act=np.argmax(act)
    if(act==0):
        a = 1.25
    elif(act ==1):
        a = 1.5
    elif(act ==2):
        a = 1.05
    elif(act ==3):
        a = 0.95   #float(s[0]-1)/float(s[0]+1)
    elif(act ==4):
        a = 0.75
    #elif(act ==3):
    #    a = 3  #float(s[0]+2)/float(s[0]+1)
    #elif(act ==4):
    #    a = 4
    #elif(act==5):
    #    a = 5
    else:
        a = 0.5
    print('a:',a)
    #print("step {}, a={}".format(j, a))
   
        #a = np.clip(np.random.normal(a1, var_my), -1, 1)
        #print("step {}, a={}".format(j, a))
    s_, r = ndnstep(a, var)

    #print("state:{}, type:{}, reward:{}, next_sate:{}".format(s, a, r, s_))
    s = s_
    j+=1
