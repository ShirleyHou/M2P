import numpy as np
import matplotlib
import matplotlib.pyplot
import scipy as sp
import scipy.io

from buildDummyNodesAndLinks import buildDummyNodesAndLinks


input_mat = scipy.io.loadmat('small_case')
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
dummy = buildDummyNodesAndLinks(nodes, links, ODmatrices)
print(i)
