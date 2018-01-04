#main program

import numpy as np
import numpy.matlib
from buildDummyNodesAndLinks import buildDummyNodesAndLinks
from buildODmatrix import buildODmatrix
from cvn2tt import cvn2tt
from DTA_MSA import DTA_MSA
import matplotlib.pyplot as plt
import math


import scipy.io

input_info = scipy.io.loadmat('info_medium.mat')
ODmatrices = input_info['ODmatrices']



input_links = input_info['links']
ID = input_links[:,0]
fromNode = input_links[:,1]-1
toNode = input_links[:,2]-1
length = input_links[:,3]
freeSpeed = input_links[:,4]
capacity = input_links[:,5]
kJam = input_links[:,6]
links = {'ID': ID.astype(np.int), 'fromNode': fromNode.astype(np.int), 'toNode': toNode.astype(np.int),
         'length': length, 'freeSpeed': freeSpeed, 'capacity': capacity, 'KJam': kJam}

input_nodes = input_info['nodes']
ID = input_nodes[:, 0]
xco = input_nodes[:, 1]
yco = input_nodes[:, 2]
nodes = {'ID': ID.astype(np.int), 'xco': xco, 'yco': yco}

nodes, links, ODmatrices = buildDummyNodesAndLinks(nodes, links, ODmatrices)

dt = 20
totT = round(20/dt)
timeSeries = np.arange(0.0,0.5*(ODmatrices.shape[1]),0.5)


ODmatrix,origins,destinations = buildODmatrix(ODmatrices,timeSeries,dt,totT)


rc_dt = 10*dt
max_It = 1
rc_agg = "last"


cvn_up,cvn_down, TF = DTA_MSA(nodes,links,origins,destinations,ODmatrix, dt, totT, rc_dt,max_It,rc_agg)

cvn2tt(np.sum(cvn_up,axis=2),np.sum(cvn_down,axis=2),dt,totT,links)

plt.xlabel("Time [h]")
plt.xlim([0,dt*totT])
plt.ylabel("Travel time [h]")
plt.show()
print("END")