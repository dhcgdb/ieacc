import math
from os import makedirs, path, write
import os
from numpy.random.mtrand import rand
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


MAX_EPISODES = 500
MAX_EP_STEPS = 500
LR_A = 0.01  # learning rate for actor
LR_C = 0.02  # learning rate for critic
GAMMA = 0.9  # reward discount
TAU = 0.01  # soft replacement
MEMORY_CAPACITY = 25000
BATCH_SIZE = 50


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


class CNet(nn.Module):  # ae(s)=a
    def __init__(self, s_dim, a_dim):
        super(CNet, self).__init__()
        self.fcs = nn.Linear(s_dim, 30)
        self.fcs.weight.data.normal_(0, 0.1)  # initialization
        self.fca = nn.Linear(a_dim, 30)
        self.fca.weight.data.normal_(0, 0.1)  # initialization
        self.out = nn.Linear(30, 1)
        self.out.weight.data.normal_(0, 0.1)  # initialization

    def forward(self, s, a):
        x = self.fcs(s)
        y = self.fca(a)
        net = F.relu(x + y)
        actions_value = self.out(net)
        return actions_value


class DDPG(object):
    def __init__(self, a_dim, s_dim):
        self.a_dim, self.s_dim, = a_dim, s_dim
        self.memory = np.zeros((MEMORY_CAPACITY, s_dim * 2 + a_dim + 1),
                               dtype=np.float32)
        self.pointer = 0
        self.observer_shape = 6
        # self.sess = tf.Session()
        self.Actor_eval = ANet(s_dim, a_dim)
        self.Actor_target = ANet(s_dim, a_dim)
        self.Critic_eval = CNet(s_dim, a_dim)
        self.Critic_target = CNet(s_dim, a_dim)
        self.ctrain = torch.optim.Adam(self.Critic_eval.parameters(), lr=LR_C)
        self.atrain = torch.optim.Adam(self.Actor_eval.parameters(), lr=LR_A)
        self.loss_td = nn.MSELoss()

    def choose_action(self, s):
        global epsilon
        global actiontype
        s = torch.unsqueeze(torch.FloatTensor(s), 0)
        if np.random.uniform() < epsilon:
            actiontype = "regular"
            return self.Actor_eval(s)[0].detach()  # ae（s）
        else:
            actiontype = "random"
            return np.random.uniform() * 2 - 1

    def learn(self):
        for x in self.Actor_target.state_dict().keys():
            eval('self.Actor_target.' + x + '.data.mul_((1-TAU))')
            eval('self.Actor_target.' + x + '.data.add_(TAU*self.Actor_eval.' +
                 x + '.data)')
        for x in self.Critic_target.state_dict().keys():
            eval('self.Critic_target.' + x + '.data.mul_((1-TAU))')
            eval('self.Critic_target.' + x +
                 '.data.add_(TAU*self.Critic_eval.' + x + '.data)')

        indices = np.random.choice(MEMORY_CAPACITY, size=BATCH_SIZE)
        bt = self.memory[indices, :]
        bs = torch.FloatTensor(bt[:, :self.s_dim])
        ba = torch.FloatTensor(bt[:, self.s_dim:self.s_dim + self.a_dim])
        br = torch.FloatTensor(bt[:, -self.s_dim - 1:-self.s_dim])
        bs_ = torch.FloatTensor(bt[:, -self.s_dim:])
        global actorloss
        global criticloss

        a = self.Actor_eval(bs)
        # loss=-q=-ce（s,ae（s））更新ae   ae（s）=a   ae（s_）=a_
        q = self.Critic_eval(bs, a)
        #print("actorq:\n", q)
        # 如果 a是一个正确的行为的话，那么它的Q应该更贴近0
        loss_a = -torch.mean(q)
        #print("actorloss:", np.double(loss_a))
        actorloss.write(str(np.double(loss_a)) + "\n")

        # print(loss_a)
        self.atrain.zero_grad()
        loss_a.backward()
        self.atrain.step()

        # 这个网络不及时更新参数, 用于预测 Critic 的 Q_target 中的 action
        a_ = self.Actor_target(bs_)
        # 这个网络不及时更新参数, 用于给出 Actor 更新参数时的 Gradient ascent 强度
        q_ = self.Critic_target(bs_, a_)
        q_target = br + GAMMA * q_  # q_target = 负的
        #print("q_target:\n", q_target)
        q_v = self.Critic_eval(bs, ba)
        #print("q_v:\n", q_v)
        td_error = self.loss_td(q_target, q_v)
        #print("criticloss:", np.double(td_error))
        criticloss.write(str(np.double(td_error)) + "\n")
        # td_error=R + GAMMA * ct（bs_,at(bs_)）-ce(s,ba) 更新ce ,但这个ae(s)是记忆中的ba，让ce得出的Q靠近Q_target,让评价更准确

        # print(td_error)
        self.ctrain.zero_grad()
        td_error.backward()
        self.ctrain.step()

    def store_transition(self, s, a, r, s_):
        transition = np.hstack((s, [a], [r], s_))
        # replace the old memory with new memory
        index = self.pointer % MEMORY_CAPACITY
        self.memory[index, :] = transition
        self.pointer += 1

    def save_model(self, i):
        save_path = './results/models/' + os.path.basename(
            __file__) + '/' + str(i)
        if (not path.isdir(save_path)):
            os.makedirs(save_path)
        torch.save(self.Actor_eval, save_path + '/Actor_eval.model')
        torch.save(self.Actor_target, save_path + '/Actor_target.model')
        torch.save(self.Critic_eval, save_path + '/Critic_eval.model')
        torch.save(self.Critic_target, save_path + '/Critic_target.model')


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


epsilon = 0.1
variance = 1
ddpg = DDPG(1, 3)
exp = Experiment(1234, 1040, "1c1p", "./")
var = Ns3AIRL(1024, NdnParam, RetScale)
actiontype = "random"

log_path = './log/' + os.path.basename(__file__)
if (not path.isdir(log_path)):
    os.makedirs(log_path)
actorloss = open(log_path + "/actorloss.txt", "w")
criticloss = open(log_path + "/criticloss.txt", "w")

print('\n\033[33mstart ddpg learning \033[0m')

for i in range(MAX_EPISODES):
    print("episode ", i)
    s = ndnreset(exp, var)
    print(s)
    ep_reward = 0
    for j in range(MAX_EP_STEPS):
        a = np.double(ddpg.choose_action(s))
        #randn = np.random.normal(a + 1, variance / (i + 1))
        #if (randn > 2.0):
        #    a = -1 + randn - 2 * np.floor(randn / 2.0)
        #elif (randn < 0.0):
        #    a = 2 - (-randn - 2 * np.floor(-randn / 2.0))
        #else:
        #    a = randn
        #a = a - 1
        print("step {}, a={}".format(j, a))
        s_, r = ndnstep(2**a, var)

        print("state:{}, type:{}, action:{}, reward:{}, next_sate:{}".format(
            s, actiontype, a, r, s_))

        ddpg.store_transition(s, a, r, s_)

        print("pool num:", ddpg.pointer)
        if ddpg.pointer > MEMORY_CAPACITY:
            ddpg.learn()
        s = s_
        ep_reward += r
    print("\033[32mepisode: {}, eprwd: {}\033[0m\n".format(i, ep_reward))
    if ddpg.pointer > MEMORY_CAPACITY:
        epsilon += 0.01
        ddpg.save_model(i)
FreeMemory()
