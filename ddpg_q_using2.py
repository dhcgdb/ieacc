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
    _fields_ = [('cWndSum', c_double), ('avgDelay', c_double),
                ('Data', c_uint32), ('InFlight', c_uint32),
                ('Nloss', c_uint32), ('Rloss', c_uint32),
                ('CLvelSum', c_uint32), ('DataSizeSum', c_uint32)]


class RetScale(Structure):
    _pack_ = 1
    _fields_ = [('newCwnd', c_double)]


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
        self.Actor_eval = torch.load(
            "results/models/ddpg_q.py/490/Actor_eval.model")
        self.Actor_target = torch.load(
            "results/models/ddpg_q.py/490/Actor_target.model")

    def choose_action(self, s):
        s = torch.unsqueeze(torch.FloatTensor(s), 0)
        return self.Actor_eval(s)[0].detach()


def ndngetstate(var):
    data = var.Acquire()
    cWnd = data.env.cWndSum
    delay = data.env.avgDelay
    acks = data.env.Data
    inflight = data.env.InFlight
    Nloss = data.env.Nloss
    Rloss = data.env.Rloss
    CLvel = data.env.CLvelSum
    DataSizeSum = data.env.DataSizeSum
    var.ReleaseAndRollback()

    avgQLength = CLvel / (acks + 0.01) / 32
    TP_Mbps = 1 + DataSizeSum * 8 / 0.2 / 1000000
    Rloss /= 100

    print([TP_Mbps, avgQLength, Rloss])

    return [np.log10(TP_Mbps), avgQLength, Rloss]


def ndnstep(a, var):
    data = var.Acquire()
    #data.act.reset= c_bool(False)
    data.act.newCwnd = a
    var.Release()
    s = ndngetstate(var)

    r = s[0] - s[1] - s[2]
    return s, r


def ndnreset(exp, var):
    exp.reset()
    exp.run(None, True)
    return ndngetstate(var)


ddpg = DDPG()
#exp = Experiment(1234, 1040, "1c3p", "./")
Init(1234,1040)
var = Ns3AIRL(1000, NdnParam, RetScale)

j = 0
#s = ndnreset(exp, var)
s=ndngetstate(var)
while (True):
    a = np.double(ddpg.choose_action(s))
    #print("s {}, a={}".format(s, a))
    s_, r = ndnstep((c_double)(2**a), var)

    #print("state:{}, type:{}, reward:{}, next_sate:{}".format(s, a, r, s_))
    s = s_
    j += 1
