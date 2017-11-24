def buildDummyNodesAndLinks(nodes, links, ODmatrices):

    import numpy as np
    new_nodes = nodes
    new_links = links
    new_ODmatrices = ODmatrices

    # Find all non empty od cells
    sum0D = ODmatrices[0, 0]
    for t in np.arange(1, ODmatrices.shape[1]):
        sum0D = sum0D + ODmatrices[0, t]

    # Origin
    origins = np.nonzero(np.sum(sum0D, axis=1) > 0)[0]
    # Destinations
    destinations = np.nonzero(np.sum(sum0D, axis=0) > 0)[0]

    # Check If Origins Only Have Outgoing Links
    issued_origins = np.empty((0, 0), dtype=int)    # Initialization
    map_dummyorigins = np.empty((0,2), dtype=int)   # Initialization
    linkToNode_list = links['toNode']
    linkFromNode_list = links['fromNode']

    for i in range(0, len(origins)):
        outgoing_links = np.nonzero(linkFromNode_list == origins[i])[0]
        incoming_links = np.nonzero(linkToNode_list == origins[i])[0]

        if outgoing_links.size==0 and incoming_links.size==0:
            print('Origin ', origins[i], ' has no incoming or outgoing links!')
        elif incoming_links.size>=1:
            issued_origins = np.append(issued_origins, origins[i])


    # Adding Dummy Origins and Dummy Connectors If Applicable
    for i in range(0, len(issued_origins)):
        new_nodes['ID'] = np.append(new_nodes['ID'], len(new_nodes['ID'])+1)
        new_nodes['xco'] = np.append(new_nodes['xco'], new_nodes['xco'].item(issued_origins[i])-10**-6)
        new_nodes['yco'] = np.append(new_nodes['yco'], new_nodes['yco'].item(issued_origins[i]) + 10 ** -6)

        new_links['ID'] = np.append(new_links['ID'], len(new_links['ID'])+1)
        new_links['fromNode'] = np.append(new_links['fromNode'], len(new_nodes['ID']))
        new_links['toNode'] = np.append(new_links['toNode'], issued_origins[i])
        new_links['length'] = np.append(new_links['length'], 0.05)
        new_links['freeSpeed'] = np.append(new_links['freeSpeed'], 60)
        new_links['capacity'] = np.append(new_links['capacity'], 10**6)
        new_links['KJam'] = np.append(new_links['KJam'], 10**6)

        map_dummyorigins = np.append(map_dummyorigins,
                                     np.expand_dims([issued_origins[i], len(new_nodes['ID'])], axis=0), axis=0)


    # Conversion of Demand From Original Origin to Dummy Origin
    for i in range(0, issued_origins.shape[0]):
        for t in range(0, ODmatrices.shape[1]):
            temp_demand = new_ODmatrices[0, t][issued_origins[i], :]
            new_ODmatrices[0, t][issued_origins[i], :] = np.zeros(new_ODmatrices[0, t].shape[1], dtype=int)
            new_ODmatrices[0, t] = np.append(new_ODmatrices[0, t], np.expand_dims(temp_demand, axis=0), axis=0)

    # check if destinations only have incoming links
    issued_destinations = np.empty((0, 0), dtype=int)    # Initialization
    map_dummydestinations = np.empty((0,2), dtype=int)   # Initialization
    for i in range(0, len(destinations)):
        outgoing_links = np.nonzero(linkFromNode_list == destinations[i])[0]
        incoming_links = np.nonzero(linkToNode_list == destinations[i])[0]

        if outgoing_links.size==0 and incoming_links.size==0:
            print('Origin ', destinations[i], ' has no incoming or outgoing links!')
        elif incoming_links.size>=1:
            issued_destinations = np.append(issued_destinations, destinations[i])

    # Adding Dummy Destinations and Dummy Connectors If Applicable
    for i in range(0, len(issued_destinations)):
        new_nodes['ID'] = np.append(new_nodes['ID'], len(new_nodes['ID'])+1)
        new_nodes['xco'] = np.append(new_nodes['xco'], new_nodes['xco'].item(issued_destinations[i])-10**-6)
        new_nodes['yco'] = np.append(new_nodes['yco'], new_nodes['yco'].item(issued_destinations[i]) + 10 ** -6)

        new_links['ID'] = np.append(new_links['ID'], len(new_links['ID'])+1)
        new_links['fromNode'] = np.append(new_links['fromNode'], len(new_nodes['ID']))
        new_links['toNode'] = np.append(new_links['toNode'], issued_destinations[i])
        new_links['length'] = np.append(new_links['length'], 0.05)
        new_links['freeSpeed'] = np.append(new_links['freeSpeed'], 60)
        new_links['capacity'] = np.append(new_links['capacity'], 10**6)
        new_links['KJam'] = np.append(new_links['KJam'], 10**6)

        map_dummydestinations = np.append(map_dummydestinations,
                                          np.expand_dims([issued_destinations[i], len(new_nodes['ID'])], axis=0), axis=0)

    # Conversion of Demand From Original Destination to Dummy Destination
    for i in range(0, issued_destinations.shape[0]):
        for t in range(0, ODmatrices.shape[1]):
            temp_demand = new_ODmatrices[0, t][:, issued_destinations[i]]
            new_ODmatrices[0, t][:, issued_destinations[i]] = np.zeros(new_ODmatrices[0, t].shape[0], dtype=int)
            # Check the Dimension coherency then Appending Based on That
            if map_dummydestinations[i, 1] > (new_ODmatrices[0, t].shape[1]+1):
                dummy = np.zeros((new_ODmatrices[0, t].shape[0],
                                  map_dummydestinations[i, 1]-new_ODmatrices[0, t].shape[1]-1), dtype=int)
                new_ODmatrices[0, t] = np.append(new_ODmatrices[0, t], dummy, axis=1)
                new_ODmatrices[0, t] = np.append(new_ODmatrices[0, t], np.expand_dims(temp_demand, axis=1), axis=1)
            elif map_dummydestinations[i, 1] == (new_ODmatrices[0, t].shape[1]+1):
                new_ODmatrices[0, t] = np.append(new_ODmatrices[0, t], np.expand_dims(temp_demand, axis=1), axis=1)
            else:
                new_ODmatrices[0, t][:, map_dummydestinations[i, 1]] = temp_demand
            # To Have a Square OD With New Number of Nodes
            if new_ODmatrices[0, t].shape[0] < new_ODmatrices[0, t].shape[1]:
                dummy = np.zeros((new_ODmatrices[0, t].shape[1]-new_ODmatrices[0, t].shape[0],
                                  new_ODmatrices[0, t].shape[1]), dtype=int)
                new_ODmatrices[0, t] = np.append(new_ODmatrices[0, t], dummy, axis=0)
            else:
                new_ODmatrices[0, t][map_dummydestinations[i, 1], :] = np.zeros((1, new_ODmatrices.shape[1]), dtype=int)
    return new_nodes, new_links, new_ODmatrices

