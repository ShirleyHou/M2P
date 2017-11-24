import numpy as np
from scipy.sparse import lil_matrix, coo_matrix, vstack, hstack


def buildDummyNodesAndLinks(nodes, links, ODmatrices):

    #local rename
    new_nodes_id = nodes.get('ID')
    new_nodes_xco = nodes.get('xco')
    new_nodes_yco = nodes.get('yco')
    new_links_id = links.get('ID')
    new_links_fromNode = links.get('fromNode')
    new_links_toNode = links.get('toNode')
    new_links_length = links.get('length')
    new_links_freeSpeed = links.get('freeSpeed')
    new_links_capacity = links.get('capacity')
    new_links_kJam = links.get('KJam')
    new_ODmatrices = ODmatrices

    #local name everything...

    #sum od matrix
    sumOD = ODmatrices[0,0];
    for i in range(1,ODmatrices.shape[1]):
        sumOD = sumOD + ODmatrices[0,i]

    #origins & destinations
    origins = np.where(np.sum(sumOD,1)>0)[0] #row  test:[12217 24186 24187] 1d array

    destinations = np.where(np.sum(sumOD,0)>0)[0] #should here be a [0] or 1?????? <---- issue

    issued_origins = []

    map_dummyorigins = []

    linkToNode_list = new_links_toNode #local rename

    linkFromNode_list = new_links_fromNode
    #.astype.

    for i in range(0,origins.shape[0]):
        outgoing_links = np.where(linkFromNode_list==origins[i])[0]
        incoming_links = np.where(linkToNode_list==origins[i])[0]
        if outgoing_links.size==0 and incoming_links.size==0:
            print('Origin '+origins[i]+' has no incoming or outgoing links!')
        elif incoming_links.size>=1:

            issued_origins.append(origins[i])

    #issued_origins = np.asarray(issued_origins)#<--change as a numpy array, delete this if list is required.

    '''
        create dummy origins & dummy connectors
    '''
    for i in range(0, len(issued_origins)): #<--test: 1 len(issued_origins)
        #add new dummy nodes element
        new_nodes_id = np.append(new_nodes_id, np.asarray(new_nodes_id.shape[0]+1))
        new_nodes_xco = np.append(new_nodes_xco, np.asarray(new_nodes_xco[issued_origins[i]]-0.000001))
        new_nodes_yco = np.append(new_nodes_yco, np.asarray(new_nodes_yco[issued_origins[i]]-0.000001))

        new_links_id = np.append(new_links_id, np.asarray(new_links_id.shape[0]+1))
        new_links_fromNode = np.append(new_links_fromNode,np.asarray(new_nodes_id.shape[0]-1))
        new_links_toNode = np.append(new_links_toNode, np.asarray(issued_origins[i]))
        new_links_length = np.append(new_links_length, np.asarray(0.05))
        new_links_freeSpeed = np.append(new_links_freeSpeed, np.asarray(60))
        new_links_capacity = np.append(new_links_capacity, np.asarray(1000000))
        new_links_kJam = np.append(new_links_kJam, np.asarray(1000000))
        map_dummyorigins.append([issued_origins[i], new_nodes_id.shape[0]])

    map_dummyorigins = np.asarray(map_dummyorigins)


    '''
     conversion of demand from originial origin to dummy origin
    '''

    addrow = 0
    for i in range(0,len(issued_origins)):

        for t in range(0, ODmatrices.shape[1]):


            temp_demand = new_ODmatrices[0,t][issued_origins[i],:]
            #NEEDTO HAVE A NEW ROW HERE.
            rows = map_dummyorigins[i,1]-new_ODmatrices[0,t].shape[0]
            cols = new_ODmatrices[0,t].shape[1]
            if(rows>0):

                addrow =addrow+1
                udpate_ODmatrices_cell=coo_matrix((rows,cols))
                new_ODmatrices[0,t]=vstack([new_ODmatrices[0,t],udpate_ODmatrices_cell]).tolil()
            #INCREMENT OF NEW ROW COMPLETED


            new_ODmatrices[0,t][issued_origins[i],:] = np.zeros((1,new_ODmatrices[0,t].shape[1]))

            new_ODmatrices[0,t][map_dummyorigins[i,1]-1,:]=temp_demand #<-- in original code here is map_dummyorigins[i,1] causing matrix overflow



    issued_destinations = []
    map_dummydestinations = []

    for i in range(0,destinations.shape[0]):

        outgoing_links = np.where(linkFromNode_list==destinations[i])[0]
        incoming_links = np.where(linkToNode_list==destinations[i])[0]

        if outgoing_links.size==0 and incoming_links.size==0:
            print('Destinations ',destinations[i],' has no incoming or outgoing links!')
        elif (incoming_links.size>=1):
            #print('get new origin in the list')
            issued_destinations.append(destinations[i])

    for i in range(0, len(issued_destinations)): #<--test: 1 len(issued_origins)
        #add new dummy nodes element
        new_nodes_id = np.append(new_nodes_id, np.asarray(new_nodes_id.shape[0]+1))
        new_nodes_xco = np.append(new_nodes_xco, np.asarray(new_nodes_xco[issued_destinations[i]]-0.000001))
        new_nodes_yco = np.append(new_nodes_yco, np.asarray(new_nodes_yco[issued_destinations[i]]-0.000001))

        new_links_id = np.append(new_links_id, np.asarray(new_links_id.shape[0]+1))
        new_links_fromNode = np.append(new_links_fromNode, np.asarray(issued_destinations[i]))
        new_links_toNode = np.append(new_links_toNode, np.asarray(new_nodes_id.shape[0]-1))
        new_links_length = np.append(new_links_length, np.asarray(0.05))
        new_links_freeSpeed = np.append(new_links_freeSpeed, np.asarray(60))
        new_links_capacity = np.append(new_links_capacity, np.asarray(1000000))
        new_links_kJam = np.append(new_links_kJam, np.asarray(1000000))
        map_dummydestinations.append([issued_destinations[i], new_nodes_id.shape[0]])

    map_dummydestinations = np.asarray(map_dummydestinations)

    for i in range(0,len(issued_destinations)):#0->1

        for t in range(0, ODmatrices.shape[1]):#0--41



            rows = new_ODmatrices[0,t].shape[0]
            cols = map_dummydestinations[i,1]-new_ODmatrices[0,t].shape[1]

            if(cols>0):

                '''
                put in extra rows and columns in each ODmatrice sparse lil_matrix.
                Hence avoiding the index overflow issue due to the immutable length property of numpy sparse matrix
                '''
                udpate_ODmatrices_cell=coo_matrix((rows, cols))
                new_ODmatrices[0,t]=hstack([new_ODmatrices[0,t],udpate_ODmatrices_cell]).tolil()
            #use hstack and vstack to complete ODmatrice reshape

            '''add new row'''



            '''add new column'''
            if(new_ODmatrices[0,t].shape[0]<new_ODmatrices[0,t].shape[1]):
                addrow =addrow+1
                udpate_ODmatrices_cell=coo_matrix((new_ODmatrices[0,t].shape[1]-new_ODmatrices[0,t].shape[0],new_ODmatrices[0,t].shape[1]))
                new_ODmatrices[0,t]=vstack([new_ODmatrices[0,t],udpate_ODmatrices_cell]).tolil()
            #use hstack and vstack to complete ODmatrice reshape


            temp_demand = new_ODmatrices[0,t][:,issued_destinations[i]]#<--needs to add a new column

            new_ODmatrices[0,t][:,issued_destinations[i]] = np.zeros((new_ODmatrices[0,t].shape[0],1))

            new_ODmatrices[0,t][:,map_dummydestinations[i,1]-1]=temp_demand

            new_ODmatrices[0,t][map_dummydestinations[i,1]-1,:]=np.zeros((1,new_ODmatrices[0,t].shape[1]))

    newlinks = {'ID': new_links_id, 'fromNode': new_links_fromNode, 'toNode': new_links_toNode,
             'length': new_links_length, 'freeSpeed': new_links_freeSpeed, 'capacity': new_links_capacity, 'KJam': new_links_kJam}
    newnodes = {'ID': new_nodes_id.astype(np.int), 'xco': new_nodes_xco, 'yco': new_nodes_yco}
    return newnodes, newlinks, new_ODmatrices