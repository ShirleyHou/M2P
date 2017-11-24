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

    #simTT OK.
    import math
    gap_dt = math.inf

    TF = []#or numpy.zeros(0)

    TF_new = allOrNothingTF(nodes_id,nodes_xco,nodes_yco,links_id,links_fromNode,links_toNode,links_length,links_freeSpeed,links_capacity,links_kJam,destinations,simTT,cvn_up,dt,totT,rc_dt,rc_agg)
    return 'test complete'


'''
    return TF, gap_dt, gap_rc
'''
def allOrNothingTF(nodes_id,nodes_xco,nodes_yco,links_id,links_fromNode,links_toNode,links_length,links_freeSpeed,links_capacity,links_kJam,destinations,simTT,cvn_up,dt,totT,rc_dt,rc_agg):
    totDest = len(destinations)
    totNodes = nodes_id.shape[0]
    totLinks = links_id.shape[0]
    strN = links_fromNode
    endN = links_toNode

    if(cvn_up.shape[0]==0):
        cvn_up =np.zeros((totLinks,totT+1,totDest))


    TF = [[None]*nodes_id.shape[0]*totT]*totDest #<--now TF is a 43*40*5 empty cell.

    print(len(TF))
    print(sum(len(x) for x in TF))
    timeSteps = dt*np.arange(0,totT+1,1)
    timeRC = rc_dt*np.arange(0,totT+1,1)
    timeRC = timeRC[timeRC<=timeSteps[-1]]

    gap = np.zeros((totLinks,totT+1))
    gap_dt= 0
    gap_rc = 0
    act_t = np.zeros(totT+1,dtype=bool) #size = (41,)
    gVeh = np.floor(rc_dt/dt)

    if rc_agg =="first":
        timeVeh = 0
    elif rc_agg == "middle":
        timeVeh = rc_dt/2
    elif rc_agg == "last":
        timeVeh = rc_dt
    elif rc_agg =='':
        #for d_index in range(0,totDest):
            #arr_map_d(d_index)
        TF = np.asarray([])
        return TF, gap_dt, gap_rc

    elif rc_agg == 'inst':
        for d_index in range(0,totDest):
            d = destinations[d_index]
            '''
            problem hereL how to construct a sparse matrix given these arguemnets?
            cannot test here
            '''
            netCostMatrix = coo_matrix((endN,strN,simTT[:,1],totNodes,totNodes))


            '''
            needs implement: dijkstra.
            '''
            #parent, distance, path = dijkstra(matrix, source, varargin)
            for n in range(0,totNodes):
                incomingLinks = np.where(endN==n)[0] #<--an array. If its [0][0] its element at one particular index
                outgoingLinks = np.where(strN==n)[0]

                #remember TF is a list
                TF[n][0][d_index]=np.zeros[max(1,incomingLinks.shape[0]),outgoingLinks.shape[0]]
                #TF[n][0][d_index][:,endN[outgoingLinks]==parent[n]]=1

            gap = []
            return TF, gap_dt, gap_rc

    tVeh = np.floor(timeVeh/dt)

    #for d_index in range(0,totDest):
        #arr_map, parent = arr_map_d(d_index)

    '''
    nested helper method
    '
    def arr_map_d(d_index):
        d = destinations[d_index]
        netCostMatrix = coo_matrix((simTT[:,-1],(endN,strN)),shape=(totNodes,totNodes))
        print(netCostMatrix)
        return arr_map, parent
    '''
    return "test allOrNothing"













#a = DTA_MSA(nodes_id,nodes_xco,nodes_yco,links_id,links_fromNode,links_toNode,links_length,links_freeSpeed,links_capacity,links_kJam,origins,destinations, ODmatrix, dt, totT, rc_dt, max_It, rc_agg);
#print(a)
'''needs complete'''
'''transform CVN values to travel times'''
#[simTT] = cvn2tt(sum(cvn_up,3),sum(cvn_down,3),dt,totT,links);
