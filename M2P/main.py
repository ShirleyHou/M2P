#main program


'''
Notice currently find no clue how to use a compiled java class in python.
The essential java class is a pair comparator,
Suggests to take a look at the Node object and write a new comparator in python.
'''
import numpy as np
from buildDummyNodesAndLinks import buildDummyNodesAndLinks
#------------------file inport --------------------#
'''import links_nodes.mat and demand.mat
Workspace 2 fields:
links_nodes.mat --> links, nodes
demand.mat --> demand
'''
#scipy module is required to inport .mat matlab workspace file
import scipy.io as sio

#load all input workspaces
load = sio.loadmat('data_sliced_reduced.mat')


#find the corrsponding name in the workspace, each name is a ndnumpy array
demand = load['demand_r']
print(demand.shape)
nodes_id = load['nodes_id']
nodes_xco = load['nodes_xco']
nodes_yco = load['nodes_yco']
links_id= load['links_id']
links_freeSpeed = load['links_freeSpeed']
links_capacity = load['links_capacity']
links_length = load['links_length']
links_toNode = load['links_toNode']
links_fromNode = load['links_fromNode']
links_kJam = load['links_kJam']


no_nodes = nodes_id.shape[0] #first dim of nodes_field
ODmatrices = np.empty((1,demand.shape[1]-2),dtype=object)

'''check all inputs are loaded correctly

print('demand: ',demand.shape)
print('links: ', links_id.shape, links_freeSpeed.shape, links_capacity.shape, \
links_length.shape, links_toNode.shape, links_fromNode.shape, links_kJam.shape)
print('nodes: ',nodes_id.shape, nodes_xco.shape, nodes_yco.shape)
print(ODmatrices.shape)
'''

nodes_id = load['nodes_id'] #find the corrsponding name in the workspace, each name is a numpy array
nodes_xco = load['nodes_xco']
nodes_yco = load['nodes_yco']
links_id= load['links_id']
links_freeSpeed = load['links_freeSpeed']
links_capacity = load['links_capacity']
links_length = load['links_length']
links_toNode = load['links_toNode']
links_fromNode = load['links_fromNode']
links_kJam = load['links_kJam']

from scipy.sparse import lil_matrix #list of list format sparse matrix, the equivalence of sparse matrix in matlab


'''generate ODmatrices'''

for i in range(0, ODmatrices.shape[1]):
    ODmatrices[0,i]=lil_matrix((no_nodes, no_nodes))
    #print(ODmatrices[0,1].shape) <-- check the size of lil_matrix

    #print(ODmatrices[0,i][1,1])
    for j in range(0, demand.shape[0]): #<1~578260

        O_node = np.where(nodes_id==demand[j,0])[0][0] #outcome of np.where is a turple--> 1st in the tuple-->number
        D_node = np.where(nodes_id==demand[j,1])[0][0] #where position 0 is the matchd index array
        #print(O_node, D_node)
        #all indices will be 1 less than the matrix in matlab, but they points to the same position.

        #the way to assign
        ODmatrices[0,i][O_node, D_node]= demand[j, i+2]



#print('ODmatrices: ',ODmatrices.shape[1])
#print(ODmatrices[0,0]+ODmatrices[0,1])#<--test whether lil matrix could be added linearly



'''@input : All nodes field, all links field, ODmatrices matrix'''

#nodes, links, ODmatrices = buildDummyNodesAndLinks(nodes_id,nodes_xco,nodes_yco,links_id,links_freeSpeed,links_capacity,links_length,links_kJam,links_toNode,links_fromNode,ODmatrices);

dt = 0.5
totT = round(20/dt)

#ODmatrix, origins, destinations = buildODmatrix(ODmatrices,timeSeries,dt,totT)

'''needs complete'''
'''set up dynamic equilibrium simulation'''
rc_dt = 10*dt
max_it = 1;
rc_agg = "last";
#[cvn_up,cvn_down,TF] = DTA_MSA(nodes,links,origins,destinations,ODmatrix,dt,totT,rc_dt,max_it,rc_agg);


'''needs complete'''
'''transform CVN values to travel times'''
#[simTT] = cvn2tt(sum(cvn_up,3),sum(cvn_down,3),dt,totT,links);


#===========function: buildDummyNodesAndLinks========
'''
Function name: buildDummyNodesAndLinks
@input: all nodes , links attributes, ODmatrices
@return: new nodes, links, ODmatrices attributes.
'''

nodes_id,nodes_xco,nodes_yco,links_id,links_fromNode,links_toNode,links_length,links_freeSpeed,links_capacity,links_kJam,ODmatrices = buildDummyNodesAndLinks(nodes_id,nodes_xco,nodes_yco,links_id,links_fromNode,links_toNode,links_length,links_freeSpeed,links_capacity,links_kJam,ODmatrices)
for i in range(0,ODmatrices.shape[1]):
    print('{1,',i,'}',ODmatrices[0,i])

dt = 0.5
totT = round(20/dt)
timeSeries = np.arange(0.0,0.5*(ODmatrices.shape[1]),0.5)


'''
Function name: buildODmatrix
@input: ODmatrices, timeSeries, dt,totT
@output: ODmatrix
'''

def buildODmatrix(ODmatrices,timeSeries,dt,totT):

    #find all non empty od cells
    sumOD = ODmatrices[0,0];
    for i in range(0,ODmatrices.shape[1]):
        sumOD = sumOD + ODmatrices[0,i]

    origins = np.where(np.sum(sumOD,1)>0)[0] #row  test:[12217 24186 24187] 1d array
    destinations = np.where(np.sum(sumOD,0)>0)[1] #col, test: [12200 19974] 1d array
    print(origins)
    print(destinations)

    timeSteps = dt*np.arange(0,totT+0.5,1)

    for t in range(0,1):
        sliceA = np.where(timeSeries<=timeSteps[t])[0] #<--smaller or equal to
        sliceA = sliceA[sliceA.size-1]

        sliceB = np.where(timeSeries<timeSteps[t+1])[0] #<--smaller
        sliceB = sliceB[sliceB.size-1]
        #print(sliceA,sliceB)
        #tempSlices = np.asarray(np.unique(sliceA,sliceB)) #<--an array
        tempSlices = np.unique(sliceA,sliceB) #<--a tuple
        print(len(tempSlices))
        if(len(tempSlices)==1):
            #print('try return')
            temp_odmatrix = ODmatrices[min(ODmatrices.shape[1],tempSlices[0])][origins,destinations]
            for i in range(0, temp_odmatrix.shape[0]):
                for j in range (0,temp_odmatrix.shape[0]):
                    od_matrix[i,j,t]=full(temp_odmatrix(i,j));

    return(destinations)
    #return ODmatrices[0,1][origins,destinations]
test = buildODmatrix(ODmatrices,timeSeries,dt,totT)
#print(test)
