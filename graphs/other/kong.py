#import matplotlib
#matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

filename_1 = '/root/ndn/proj-sep/aimd_sta_afd-loss1.txt'
filename_3 = '/root/ndn/proj-sep/aimd_sta_afd-loss1-1.txt'


with open(filename_1, 'r') as f:
    contents = f.read()
    contents = contents.replace(' ','') 

with open(filename_3, 'w') as f1:
    f1.write(contents)

    