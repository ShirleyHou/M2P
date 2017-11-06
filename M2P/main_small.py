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
rc_dt = 10*dt
max_It = 1
rc_agg = "last"


from scipy.interpolate import interp1d
def DTA_MSA(nodes_id,nodes_xco,nodes_yco,links_id,links_fromNode,links_toNode,links_length,links_freeSpeed,links_capacity,links_kJam,origins,destinations, ODmatrix, dt, totT, rc_dt, maxIt, rc_agg):


    #pass in all variables.
    '''
    Todo:
    semilogy graph plotting!
    '''
    #start_time = cputime <-- should I record this?

    if not maxIt: #<--unlikely becasue this input is compulsary.
        maxIt= 20

    #initialization
    totNodes = nodes_id.shape[0] #<--row.
    totLinks = links_toNode.shape[0]
    totDest= destinations.shape[0] #<--only 1 dimension, or len(destinations), if in form of a list.

    cvn_up = np.zeros((totLinks,totT+1, totDest))
    cvn_down = np.zeros((totLinks,totT+1, totDest))

    it = 0
    if(cvn_up.ndim>3):
        simTT = cvn2tt(np.sum(cvn_up,2), np.sum(cvn_up,2),dt,totT,links_id,links_fromNode,links_toNode,links_length,links_freeSpeed,links_capacity,links_kJam)
    else:
        simTT = cvn2tt(cvn_up, cvn_up,dt,totT,links_id,links_fromNode,links_toNode,links_length,links_freeSpeed,links_capacity,links_kJam)

    '''
    build cvn2tt here!
    '''
    #gap_dt = inf
    TF = []#or numpy.zeros(0)




def cvn2tt(cvn_up, cvn_down, dt, totT, links_id,links_fromNode,links_toNode,links_length,links_freeSpeed,links_capacity,links_kJam):

    simTT = np.zeros((links_id.shape[0],totT+1))#<--length of the links_id

    timeSteps = dt*np.arange(0,totT+1, 1)

    #OK simTT & timeSteps

    for l in range(0, links_id.shape[0]):
        down, iun = np.unique(cvn_down[l,:], return_index=True)
        if down.shape[0]<=1:
            simTT[l,:]=links_length[l]/links_freeSpeed[l]
        else:
            simTT[l,:]= interp1d(down,timeSteps[iun])(cvn_up[l,:])-dt*np.arrange(0,totT+1,1)







[cvn_up,cvn_down,TF] = DTA_MSA(nodes_id,nodes_xco,nodes_yco,links_id,links_fromNode,links_toNode,links_length,links_freeSpeed,links_capacity,links_kJam,origins,destinations, ODmatrix, dt, totT, rc_dt, max_It, rc_agg);

'''needs complete'''
'''transform CVN values to travel times'''
#[simTT] = cvn2tt(sum(cvn_up,3),sum(cvn_down,3),dt,totT,links);





