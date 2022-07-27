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


activelabel = [False, False, False, False]


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
    return [cWnd, delay]


def ndnstep(a, var):
    data = var.Acquire()
    #data.act.reset= c_bool(False)
    data.act.newCwnd = a
    var.Release()
    return ndngetstate(var)


def ndnreset(exp):
    setting = {"SimulatorImplementationType": "ns3::VisualSimulatorImpl"}
    exp.reset()
    exp.run(None, True)


def actualrun(var, index):
    logfile = open("./log/multiport/ne" + str(index) + ".log", "w")
    s = ndngetstate(var)
    global activelabel
    j = 0
    while (True):
        if (s[1] == 1.0): activelabel[index] = True
        if (s[1] == -1.0): activelabel[index] = False
        num = activelabel.count(True)
        if (num == 0): num == 1
        print(index, s, activelabel)
        a = s[0] * 20000 / 8 / 1024 / num
        logfile.write("s={}, a={}\n".format(s, a))
        s = ndnstep((c_double)(a), var)
        j += 1


exp = Experiment(1234, 1040, "2point", "./")
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
thread1.start()
#thread2.start()
#thread3.start()