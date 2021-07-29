import math
from os import makedirs, path, write
import os
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
    ]


class RetScale(Structure):
    _pack_ = 1
    _fields_ = [('reset', c_bool), ('newCwnd', c_double)]

class ANet(nn.Module):
    def __init__(self, s_dim, a_dim):
        super(ANet, self).__init__()
        self.fc1 = nn.Linear(s_dim, 30)
        self.fc1.weight.data.normal_(0, 0.1)
        self.out = nn.Linear(30, a_dim)
        self.out.weight.data.normal_(0, 0.1)

    def forward(self, x):
        x = self.fc1(x)
        x = F.relu(x)
        x = self.out(x)
        # x = F.tanh(x)
        x = torch.tanh(x)
        actions_value = x
        return actions_value

class DDPG(object):
    def __init__(self):
        self.Actor_eval = torch.load("results/models/320/Actor_eval.model")
        self.Actor_target = torch.load("results/models/320/Actor_target.model")

    def choose_action(self, s):
        s = torch.unsqueeze(torch.FloatTensor(s), 0)
        return self.Actor_eval(s)[0].detach()


def ndngetstate(var):
    data = var.Acquire()
    cWnd = data.env.cWnd
    delay = data.env.avgDelay
    acks = data.env.Data
    inflight = data.env.InFlight
    Rloss = data.env.Rloss
    var.ReleaseAndRollback()

    acks = acks / 234
    delay = (0.089 - delay) / 0.028
    return [acks, delay]


def ndnstep(a, var):
    data = var.Acquire()
    data.act.newCwnd =a
    var.Release()
    s = ndngetstate(var)

    r = s[0] + s[1]
    return s, r


def ndnreset(exp, var):
    exp.reset()
    exp.run(None, True)
    return ndngetstate(var)


ddpg = DDPG()
FreeMemory()
exp = Experiment(1234, 4096, "main", "./")
var = Ns3AIRL(1024, NdnParam, RetScale)

j=0
s = ndnreset(exp, var)
while(True):
    a = np.double(ddpg.choose_action(s))
    #print("step {}, a={}".format(j, a))
    s_, r = ndnstep((c_double)(2**a), var)

    #print("state:{}, type:{}, reward:{}, next_sate:{}".format(s, a, r, s_))
    s = s_
    j+=1
