#main program


'''
Notice currently find no clue how to use a compiled java class in python.
The essential java class is a pair comparator,
Suggests to take a look at the Node object and write a new comparator in python.
'''
import numpy as np
from buildDummyNodesAndLinks import buildDummyNodesAndLinks
from buildODmatrix import buildODmatrix
#------------------file inport --------------------#

#scipy module is required to inport .mat matlab workspace file
import scipy.io as sio

#load all input workspaces
load = sio.loadmat('MS-DTA/small_case.mat')


#find the corrsponding name in the workspace, each name is a ndnumpy array

ODmatrices = load['ODmatrices']
nodes = load['nodes']
links = load['links']
links_id = links[:,0]-1 #<--to match with python index style.

links_fromNode = np.zeros((links_id.shape[0]))
links_toNode = np.zeros((links_id.shape[0]))
for i in range(0, links_id.shape[0]):
    links_fromNode[i]=np.where(nodes[:,0]==links[i,1])[0][0]
    links_toNode[i] = np.where(nodes[:,0]==links[i,2])[0][0]

links_length = links[:,3]
links_freeSpeed = links[:,4]
links_capacity = links[:,5]
links_kJam = links[:,6]

nodes = load['nodes']
original_node_id = nodes[:,0]
nodes_id = np.arange(0,nodes.shape[0])
nodes_xco = nodes[:,1]
nodes_yco = nodes[:,2]





from scipy.sparse import lil_matrix #list of list format sparse matrix, the equivalence of sparse matrix in matlab



#===========function: buildDummyNodesAndLinks========
'''
Function name: buildDummyNodesAndLinks
@input: all nodes , links attributes, ODmatrices
@return: new nodes, links, ODmatrices attributes.
'''
nodes_id,nodes_xco,nodes_yco,links_id,links_fromNode,links_toNode,links_length,links_freeSpeed,links_capacity,links_kJam,ODmatrices = buildDummyNodesAndLinks(nodes_id,nodes_xco,nodes_yco,links_id,links_fromNode,links_toNode,links_length,links_freeSpeed,links_capacity,links_kJam,ODmatrices)

#------------------OK--------------

#==================end of function===================

dt = 0.5
totT = round(20/dt)
timeSeries = np.arange(0.0,0.5*(ODmatrices.shape[1]),0.5)

#===========function: buildOdmatrix==================
'''
Function name: buildODmatrix
@input: ODmatrices, timeSeries, dt,totT
@output: ODmatrix
'''

ODmatrix,origins,destinations = buildODmatrix(ODmatrices,timeSeries,dt,totT)

#--------------OK--------------

#==================end of function===================
'''needs complete'''
'''set up dynamic equilibrium simulation'''
#rc_dt = 10*dt
#max_it = 1
#rc_agg = "last"
#[cvn_up,cvn_down,TF] = DTA_MSA(nodes,links,origins,destinations,ODmatrix,dt,totT,rc_dt,max_it,rc_agg);


'''needs complete'''
'''transform CVN values to travel times'''
#[simTT] = cvn2tt(sum(cvn_up,3),sum(cvn_down,3),dt,totT,links);





