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
    _fields_ = [('time_s', c_double), ('faceCwndMax', c_double * 3),
                ('facePending', c_int * 3), ('faceDataNum', c_int * 3),
                ('faceRttEstm', c_double * 3)]


class RetScale(Structure):
    _pack_ = 1
    _fields_ = [('faceActVal', c_double * 3)]


MAX_EPISODES = 500
MAX_EP_STEPS = 300
LR_A = 0.01  # learning rate for actor
LR_C = 0.02  # learning rate for critic
GAMMA = 0.9  # reward discount
TAU = 0.01  # soft replacement
MEMORY_CAPACITY = 10000
BATCH_SIZE = 32


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
            return self.Actor_eval(s).detach().squeeze()  # ae（s）
        else:
            actiontype = "random"
            return [
                np.random.uniform() * 2 - 1,
                np.random.uniform() * 2 - 1,
                np.random.uniform() * 2 - 1
            ]

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
        transition = np.hstack((s, a, [r], s_))
        # replace the old memory with new memory
        index = self.pointer % MEMORY_CAPACITY
        self.memory[index, :] = transition
        self.pointer += 1

    def save_model(self, i):
        save_path = './results/mp_models/' + str(i)
        if (not path.isdir(save_path)):
            os.makedirs(save_path)
        torch.save(self.Actor_eval, save_path + '/Actor_eval.model')
        torch.save(self.Actor_target, save_path + '/Actor_target.model')
        torch.save(self.Critic_eval, save_path + '/Critic_eval.model')
        torch.save(self.Critic_target, save_path + '/Critic_target.model')


def ndngetstate(var):
    meanTP = [0, 0, 0]
    data = var.Acquire()
    time_s = data.env.time_s
    faceCwndMax = data.env.faceCwndMax
    facePending = data.env.facePending
    faceDataNum = data.env.faceDataNum
    faceRttEstm = data.env.faceRttEstm
    var.ReleaseAndRollback()
    for i in [0, 1, 2]:
        meanTP[i] = faceDataNum[i] * 0.00008192 / time_s
    return [
        meanTP[0], faceRttEstm[0], meanTP[1], faceRttEstm[1], meanTP[2],
        faceRttEstm[2]
    ]


def ndnstep(a, var):
    data = var.Acquire()
    data.act.faceActVal[0] = 2**a[0]
    data.act.faceActVal[1] = 2**a[1]
    data.act.faceActVal[2] = 2**a[2]
    var.Release()
    s = ndngetstate(var)
    r = s[0] / s[1] + s[2] / s[3] + s[4] / s[5]
    return s, r


def ndnreset(exp, var):
    exp.reset()
    exp.run(None, True)
    return ndngetstate(var)


epsilon = 0.1
ddpg = DDPG(3, 6)
exp = Experiment(1234, 1080, "multiport", "./")
var = Ns3AIRL(1024, NdnParam, RetScale)
actiontype = "random"

actorloss = open("actorloss_mp.txt", "w")
criticloss = open("criticloss_mp.txt", "w")

print('start ddpg learning')

for i in range(MAX_EPISODES):
    epsilon += 0.003
    print("episode ", i)
    s = ndnreset(exp, var)
    print(s)
    ep_reward = 0
    for j in range(MAX_EP_STEPS):
        a = np.array(ddpg.choose_action(s))
        print(a)
        #a = np.clip(np.random.normal(a1, var_my), -1, 1)
        print("step:{},actType:{}".format(j, actiontype))
        s_, r = ndnstep(a, var)
        #print("state:{}, type:{}, action:{}, reward:{}, next_sate:{}".format(
        #s, actiontype, a, r, s_))
        ddpg.store_transition(s, a, r, s_)
        print("reward:", r, "pool num:", ddpg.pointer)
        if ddpg.pointer > MEMORY_CAPACITY:
            ddpg.learn()
        s = s_
        ep_reward += r
    print("episode: {}, eprwd: {}\n\n\n\n".format(i, ep_reward))
    ddpg.save_model(i)
FreeMemory()
