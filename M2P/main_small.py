#main program

import numpy as np
import numpy.matlib
from buildDummyNodesAndLinks import buildDummyNodesAndLinks
from buildODmatrix import buildODmatrix
from cvn2tt import cvn2tt
from DTA_MSA import DTA_MSA
import matplotlib.pyplot as plt
import math
plt.close("all")

#------------------file inport --------------------#

#scipy module is required to inport .mat matlab workspace file
import scipy.io

input_mat = scipy.io.loadmat('info2_small.mat')
nodes = input_mat['nodes']
links = input_mat['links']
ODmatrices = input_mat['ODmatrices']

ID = links[:, 0]
ID = np.expand_dims(ID, axis=1)


fromNode = np.array([])
toNode = np.array([])
for i in range(links.shape[0]):
    dummy = np.nonzero(nodes[:, 0] == links[i, 1])[0]
    fromNode = np.append(fromNode, dummy)
    dummy = np.nonzero(nodes[:, 0] == links[i, 2])[0]
    toNode = np.append(toNode, dummy)

length = links[:, 3]
freeSpeed = links[:, 4]
capacity = links[:, 5]
KJam = links[:, 6]
links = {'ID': ID.astype(np.int), 'fromNode': fromNode.astype(np.int), 'toNode': toNode.astype(np.int),
         'length': length, 'freeSpeed': freeSpeed, 'capacity': capacity, 'KJam': KJam}


original_node_id = nodes[:, 0]
ID = np.arange(1, nodes.shape[0]+1)
xco = nodes[:, 1]
yco = nodes[:, 2]
nodes = {'ID': ID.astype(np.int), 'xco': xco, 'yco': yco}






nodes, links, ODmatrices = buildDummyNodesAndLinks(nodes, links, ODmatrices)
dt = 0.5
totT = round(20/dt)
timeSeries = np.arange(0.0,0.5*(ODmatrices.shape[1]),0.5)

ODmatrix,origins,destinations = buildODmatrix(ODmatrices,timeSeries,dt,totT)

from scipy.interpolate import interp1d


rc_dt = 10*dt
max_It = 10
rc_agg = "last"



cvn_up,cvn_down, TF = DTA_MSA(nodes,links,origins,destinations,ODmatrix, dt, totT, rc_dt,max_It,rc_agg)


simTT = cvn2tt(np.sum(cvn_up,axis=2),np.sum(cvn_down,axis=2),dt,totT,links)

plt.figure()
for t in range(0,50):
    plt.plot(dt*np.linspace(0,totT,num=totT+1),simTT[t,:])


plt.xlabel("Time [h]")
plt.xlim([0,dt*totT])
plt.ylabel("Travel time [h]")
plt.show()
print("END")
