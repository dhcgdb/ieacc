import sys
from py_interface import *
from ctypes import *
import torch
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
import threading


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
    if (var == None):
        return None
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

    if (acks != 0): avgQLength = CLvel / acks / 32
    else: avgQLength = 0.5
    TP_Mbps = 1 + DataSizeSum * 8 / 0.2 / 1000000
    Rloss = Rloss / 100

    return [np.log10(TP_Mbps), avgQLength, Rloss]


def ndnstep(a, var):
    data = var.Acquire()
    #data.act.reset= c_bool(False)
    data.act.newCwnd = a
    var.Release()
    s = ndngetstate(var)

    r = s[0] - s[1] - s[2]
    return s, r


def ndnreset(exp):
    global nrun
    setting = {"--SimulatorImplementationType": "ns3::VisualSimulatorImpl"}
    arg = {nrun: ""}
    exp.reset()
    exp.run(None, True,{'LD_LIBRARY_PATH': '../../lib/lib/'})


def actualrun(var, index):
    logfile = open("./log/spec/ddpg_DELAY" + str(index) + ".log", "w")
    ddpg = DDPG()
    s = ndngetstate(var)
    j = 0
    while (True):
        a = np.double(ddpg.choose_action(s))
        s[0] = 10**s[0]
        s[1] = s[1] * 32
        logfile.write("s={}, a={}\n".format(s, a))
        logfile.flush()
        s, r = ndnstep((c_double)(2**a), var)
        j += 1

nrun=''
if(len(sys.argv)>1):
    nrun=sys.argv[1]
exp = Experiment(1234, 1040, "./build/1c1p", "./")
var0 = Ns3AIRL(500, NdnParam, RetScale)
var1 = Ns3AIRL(501, NdnParam, RetScale)
var2 = Ns3AIRL(502, NdnParam, RetScale)
var3 = Ns3AIRL(503, NdnParam, RetScale)

ndnreset(exp)
thread0 = threading.Thread(target=actualrun, args=(var0, 0))
thread1 = threading.Thread(target=actualrun, args=(var1, 1))
thread2 = threading.Thread(target=actualrun, args=(var2, 2))
thread3 = threading.Thread(target=actualrun, args=(var3, 3))

thread0.start()
#thread1.start()
#thread2.start()
#thread3.start()