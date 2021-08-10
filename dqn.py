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
MAX_EP_STEPS = 500
LR = 0.01  # learning rate 
GAMMA = 0.9  # reward discount
MEMORY_CAPACITY = 10000
BATCH_SIZE = 32

epsilon = 0.1
#Reset()
exp = Experiment(1234, 2120, "1c1p", "./")
var = Ns3AIRL(1024, NdnParam, RetScale)
actiontype = "random"

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

N_action = 6
N_state = 4
class DQN(object):
    def __init__(self, a_dim, s_dim):
        self.a_dim, self.s_dim, = a_dim, s_dim
        self.memory = np.zeros((MEMORY_CAPACITY, s_dim * 2 + 1 + 1),
                               dtype=np.float32)
        self.pointer = 0
        self.learn_step_couter = 0
        self.observer_shape = N_action+1+N_state*2
        # self.sess = tf.Session()
        self.eval_net = Net(s_dim, a_dim)
        self.target_net = Net(s_dim, a_dim)

        self.optimizer = torch.optim.Adam(self.eval_net.parameters(), lr=LR)
        self.loss_td = nn.MSELoss()

    def choose_action(self, s):
        global epsilon
        global actiontype
        s = torch.unsqueeze(torch.FloatTensor(s), 0)
        if np.random.uniform() < epsilon:
            actiontype = "regular"
            actions_value = self.eval_net.forward(s)
            print('action_value:',actions_value)
            action = torch.max(actions_value,1)[1].data.numpy()
            print('regular action:',action)
            action=action[0]
            #print('regular action:',action)

            return action  # ae（s）
        else:
            actiontype = "random"
            action = np.random.randint(0,6)
            print('random action:',action)
            return action

    def learn(self):
        if self.learn_step_couter % MAX_EP_STEPS ==0:
            self.target_net.load_state_dict(self.eval_net.state_dict())
        self.learn_step_couter += 1

        indices = np.random.choice(MEMORY_CAPACITY, size=BATCH_SIZE)
        bt = self.memory[indices, :]
        bs = torch.FloatTensor(bt[:, :self.s_dim])
        ba = torch.LongTensor(bt[:, self.s_dim:self.s_dim +1].astype(int))
        br = torch.FloatTensor(bt[:, self.s_dim +1:self.s_dim+2])
        bs_ = torch.FloatTensor(bt[:, -self.s_dim:])
        global loss_a

        q_eval = self.eval_net(bs).gather(1,ba)
        # loss=-q=-ce（s,ae（s））更新ae   ae（s）=a   ae（s_）=a_
        q_next = self.target_net(bs_).detach()
        #print('q_next:',q_next)
        #print('q_next.max(1)[0]',q_next.max(1)[0])
        #print('q_next.max(1)[0].view(BATCH_SIZE,1)',q_next.max(1)[0].view(BATCH_SIZE,1))
        next_state =q_next.max(1)[0].view(BATCH_SIZE,1)  #detach()
        #print('br:',br)
        q_target = br + 0.9 * next_state
        #print("actorq:\n", q)
        # 如果 a是一个正确的行为的话，那么它的Q应该更贴近0
        loss = self.loss_td(q_eval,q_target)
        #print("actorloss:", np.double(loss_a))
        loss_a.write(str(np.double(loss)) + "\n")

        # print(loss_a)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    def store_transition(self, s, a, r, s_):
        transition = np.hstack((s, [a], [r], s_))
        # replace the old memory with new memory
        index = self.pointer % MEMORY_CAPACITY
        self.memory[index, :] = transition
        self.pointer += 1

    def save_model(self, i):
        save_path = './results/dqn_model_4/' + str(i)
        if (not path.isdir(save_path)):
            os.makedirs(save_path)
        torch.save(self.eval_net, save_path + '/eval_net.model')
        torch.save(self.target_net, save_path + '/target_net.model')
       

def ndngetstate(var):
    data = var.Acquire()
    cWnd = data.env.cWnd
    delay = data.env.avgDelay
    acks = data.env.Data
    inflight = data.env.InFlight
    Rloss = data.env.Rloss
    #Ninter = data.env.Ninter
    var.ReleaseAndRollback()
    print('cWnd:',cWnd,',acks:',acks,',delay:',delay,',Rloss:',Rloss)
    #acks = acks / 700
    #delay = (0.13 - delay) / 0.11
    return [cWnd/601.0,float(acks)/350.0, delay,float(Rloss)/20.0]


def ndnstep(a, var):
    data = var.Acquire()
    data.act.newCwnd = c_double(a)
    var.Release()
    s = ndngetstate(var)

    r = s[0]+s[1]-10*s[2]-s[3]*2.92 #-float(s[3])/32.0
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


dqn = DQN(6, 4)

loss_a = open("loss.txt", "w")


print('\n\n\n\nstart dqn learning')

for i in range(MAX_EPISODES):
    epsilon += 0.003
    print("episode ", i)
    s = ndnreset(exp, var)
    print(s)
    ep_reward = 0
    for j in range(MAX_EP_STEPS):
        act = dqn.choose_action(s)
        #print("step {}, a={}".format(j, act))
        if(act==0):
            a = 1.25
        elif(act ==1):
            a = 1.5
        elif(act ==2):
            a = 1.005
        elif(act ==3):
            a = 0.995   #float(s[0]-1)/float(s[0]+1)
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
        print('act: ',act,'a: ',a)
        #a = np.clip(np.random.normal(a1, var_my), -1, 1)
        #print("step {}, a={}".format(j, a))
        s_, r = ndnstep(a, var)

        print("state:{}, type:{}, action:{}, reward:{}, next_sate:{}".format(
            s, actiontype, a, r, s_))

        dqn.store_transition(s, act, r, s_)

        print("pool num:", dqn.pointer)
        if dqn.pointer > MEMORY_CAPACITY:
            dqn.learn()
        s = s_
        ep_reward += r
    print("episode: {}, eprwd: {}\n\n\n\n".format(i, ep_reward))
    dqn.save_model(i)
FreeMemory()
