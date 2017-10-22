import numpy as np



def buildDummyNodesAndLinks(nodes_id,nodes_xco,nodes_yco,links_id,links_fromNode,links_toNode,links_length,links_freeSpeed,links_capacity,links_kJam,ODmatrices):
    '''
    issue: line 81, line 122, have index error when transfering from matlab code.
    '''
    #local rename
    new_nodes_id = nodes_id;
    new_nodes_xco = nodes_xco;
    new_nodes_yco = nodes_yco;
    new_links_id = links_id;
    new_links_fromNode = links_fromNode
    new_links_toNode = links_toNode
    new_links_length = links_length
    new_links_freeSpeed = links_freeSpeed
    new_links_capacity = links_capacity
    new_links_kJam = links_kJam
    new_ODmatrices = ODmatrices
    #local name everthing...

    #sum od matrix
    sumOD = ODmatrices[0,0];
    for i in range(1,ODmatrices.shape[1]):
        sumOD = sumOD + ODmatrices[0,i]

    #origins & destinations
    origins = np.where(np.sum(sumOD,1)>0)[0] #row  test:[12217 24186 24187] 1d array
    destinations = np.where(np.sum(sumOD,0)>0)[1] #col, test: [12200 19974] 1d array

    issued_origins = []
    map_dummyorigins = []
    linkToNode_list = links_toNode #local rename
    linkFromNode_list = links_fromNode


    for i in range(0,origins.shape[0]):
        outgoing_links = np.where(linkFromNode_list==origins[i])[0]
        incoming_links = np.where(linkToNode_list==origins[i])[0]
        if outgoing_links.size==0 and incoming_links.size==0:
            print('Origin '+origins[i]+' has no incoming or outgoing links!')
        elif incoming_links.size>=1:
            #print('get new origin in the list')
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
        new_links_fromNode = np.append(new_links_fromNode, np.asarray(new_nodes_id.shape[0]))
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
    #print('new_ODmatrices',new_ODmatrices.shape)

    for i in range(0,len(issued_origins)):#0->1

        for t in range(0, ODmatrices.shape[1]):#0--41

            temp_demand = new_ODmatrices[0,t][issued_origins[i],:]

            new_ODmatrices[0,t][issued_origins[i],:] = np.zeros((1,new_ODmatrices[0,t].shape[1]))

            new_ODmatrices[0,t][map_dummyorigins[i,0],:]=temp_demand #<-- in original code here is map_dummyorigins[i,1] causing matrix overflow


    issued_destinations = []
    map_dummydestinations = []

    for i in range(0,destinations.shape[0]):

        outgoing_links = np.where(linkFromNode_list==destinations[i])[0]
        incoming_links = np.where(linkToNode_list==destinations[i])[0]

        if outgoing_links.size==0 and incoming_links.size==0:
            print('Destinations '+destinations[i]+' has no incoming or outgoing links!')
        elif (incoming_links.size>=1):
            #print('get new origin in the list')
            issued_destinations.append(destinations[i])

    for i in range(0, len(issued_destinations)): #<--test: 1 len(issued_origins)
        #add new dummy nodes element
        new_nodes_id = np.append(new_nodes_id, np.asarray(new_nodes_id.shape[0]+1))
        new_nodes_xco = np.append(new_nodes_xco, np.asarray(new_nodes_xco[issued_destinations[i]]-0.000001))
        new_nodes_yco = np.append(new_nodes_yco, np.asarray(new_nodes_yco[issued_destinations[i]]-0.000001))

        new_links_id = np.append(new_links_id, np.asarray(new_links_id.shape[0]+1))
        new_links_fromNode = np.append(new_links_fromNode, np.asarray(new_nodes_id.shape[0]))
        new_links_toNode = np.append(new_links_toNode, np.asarray(issued_destinations[i]))
        new_links_length = np.append(new_links_length, np.asarray(0.05))
        new_links_freeSpeed = np.append(new_links_freeSpeed, np.asarray(60))
        new_links_capacity = np.append(new_links_capacity, np.asarray(1000000))
        new_links_kJam = np.append(new_links_kJam, np.asarray(1000000))
        map_dummydestinations.append([issued_destinations[i], new_nodes_id.shape[0]])

    map_dummydestinations = np.asarray(map_dummydestinations)

    for i in range(0,len(issued_destinations)):#0->1

        for t in range(0, ODmatrices.shape[1]):#0--41

            temp_demand = new_ODmatrices[0,t][issued_destinations[i],:]

            new_ODmatrices[0,t][issued_destinations[i],:] = np.zeros((1,new_ODmatrices[0,t].shape[1]))

            new_ODmatrices[0,t][map_dummydestinations[i,0],:]=temp_demand #<-- in original code here is map_dummyorigins[i,1] causing matrix overflow

    return new_nodes_id, new_nodes_xco, new_nodes_yco, new_links_id, new_links_fromNode, new_links_toNode, new_links_length,new_links_freeSpeed, new_links_capacity, new_links_kJam, new_ODmatrices
