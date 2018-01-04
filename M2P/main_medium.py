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

#info2 = 'info2_medium_t2a.mat'
#info3 = 'info3_medium_t2a.mat'
info2 = 'info2_small.mat'
info3 = 'info3_small_30.mat'
#infoM = 'info_medium.mat' <--used for testing buildOD matrix functions

input_info = scipy.io.loadmat(info3)
input_info2 = scipy.io.loadmat(info2)
ODmatrices = input_info2['ODmatrices']

dt = 20
totT = round(20/dt)
timeSeries = np.arange(0.0,0.5*(ODmatrices.shape[1]),0.5)


#nodes, links, ODmatrices = buildDummyNodesAndLinks(nodes, links, ODmatrices)

#ODmatrix,origins,destinations = buildODmatrix(ODmatrices,timeSeries,dt,totT)

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

origins = input_info['origins'][0]-1
destinations = input_info['destinations'][0]-1


ODmatrix = input_info['ODmatrix']



if ODmatrix.ndim==2:
    ODmatrix = np.expand_dims(ODmatrix, axis=2)




rc_dt = 10*dt
max_It = 1
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