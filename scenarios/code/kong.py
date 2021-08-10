#import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

filename_1 = '/root/ndnproj-0707/ndnproj/results/single-static-data/50m-50-ddpg.txt'
filename_2 = '/root/ndnproj-0707/ndnproj/results/single-static-data/50m-50-ddpg-dyn.txt'
filename_3 = '/root/ndnproj-0707/ndnproj/results/single-static-data/50m-50-ddpg-1.txt'
filename_4 = '/root/ndnproj-0707/ndnproj/results/single-static-data/50m-50-ddpg-dyn-1.txt'

with open(filename_1, 'r') as f:
    contents = f.read()
    contents = contents.replace(' ','') 

with open(filename_3, 'w') as f1:
    f1.write(contents)

with open(filename_2, 'r') as f:
    contents = f.read()
    contents = contents.replace(' ','') 

with open(filename_4, 'w') as f1:
    f1.write(contents)
    