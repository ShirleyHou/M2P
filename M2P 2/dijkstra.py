import numpy as np
import scipy as sp
import scipy.sparse as sparse
import scipy.io

def dijkstra(matrix, source):
    '''
    dummy = scipy.io.loadmat('matrix')
    SparsePy = sparse.csr_matrix((dummy['matrix'].data, dummy['matrix'].indices, dummy['matrix'].indptr),
                                 dummy['matrix'].shape)
    SparsePy = SparsePy.T


    matrixPy = sparse.csr_matrix((dummy['matrix'].data, dummy['matrix'].indices, dummy['matrix'].indptr),
                                 dummy['matrix'].shape).todense()
    matrixPy = matrixPy.T
    '''
    SparsePy = matrix.tocsr()
    matrixPy = SparsePy.todense()
    n = matrixPy.shape[0]
    parents = np.zeros((n, 1))
    distance = np.full((n, 1), np.inf)
    visited = np.full([n, 1], np.False_)


    # Add the source node the list
    nodesQueue = np.array([0, source])
    nodesQueue = np.expand_dims(nodesQueue, axis=1)

    if True:

        # If no destination node is provided the algorithm runs until all nodes are labeled
        maxnum = nodesQueue.size

        while nodesQueue.size > 0:
            dummy = np.argmin(nodesQueue[0, :])
            elem = nodesQueue[:, dummy]
            nodesQueue = np.delete(nodesQueue, dummy, axis=1)
            u = elem[1].astype(int)
            k = elem[0]
            # If it is already visited ignore it
            if visited[u]:
                continue
            # Fix the distance
            distance[u] = k
            visited[u] = True
            # Go over all unvisited neighbours
            ind = sparse.find(SparsePy[u, :])
            nv = ind[1]
            s = ind[2]
            for i in range(nv.size):
                v = nv[i]
                if np.logical_not(visited[v]):
                    temp = s[i] + distance[u]
                    if temp < distance[v]:
                        # If a new value is found it is added to the list
                        if nodesQueue.shape[1]==0:
                            nodesQueue = np.array([[temp[0]], [v]])
                        else:
                            nodesQueue = np.append(nodesQueue, np.array([[temp[0]], [v]]), axis=1)
                        distance[v] = temp
                        parents[v] = u
        path = np.array([])
    else:
        print("DIJKSTRA FUNC: It wll not applicable in this code version")

    parents = np.transpose(parents.squeeze())
    distance = np.transpose(distance.squeeze())
    return parents, distance, path