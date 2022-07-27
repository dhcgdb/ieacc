import matplotlib

matplotlib.use('cairo')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.figure(figsize=(4.5, 4.0))

colorset = ['red', '#1A6FDF', '#37AD6B', '#CC9900']
styleset = ['-', ':', '--', '-.']
nameset = ['IEACC', 'ICP', 'ECP', 'DRL-CCP']
prefixset = ['ddpg', 'aimd', 'ecp', 'dqn']
pointset = ['o', 'v', 'D', 's']


def getKey(elem):
    if (len(elem) > 3 and elem[0] == 'time'):
        return float(elem[1])
    else:
        return float('inf')


prefixset = ['ddpg', 'dqn']
suffixset = ['100', '91', '82', '73', '64']
targetnum = 450000
figparami = 0
a = []
for suffix in suffixset:
    for prefix in prefixset:
        filename1 = '/root/ndn/proj-sep/log/reexp/' + prefix + '-c1-' + suffix + '-4.log'
        filename2 = '/root/ndn/proj-sep/log/reexp/' + prefix + '-c0-4.log'
        num = 0
        tocompindex = 0
        lines = open(filename1, 'r').readlines() + open(filename2,
                                                        'r').readlines()
        valueset = []
        for line in lines:
            value = line.replace(' ', '').split(',')
            valueset.append(value)
        print(prefix + suffix,"sorting")
        valueset.sort(key=getKey)
        print(prefix + suffix,"sorting end")
        for value in valueset:
            if (len(value) >= 3 and value[2] == 'data'):
                num += 1
                if (num == targetnum):
                    a.append((prefix + suffix, value[1]))
                    break
print(a)