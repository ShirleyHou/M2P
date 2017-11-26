#main program


'''
Notice currently find no clue how to use a compiled java class in python.
The essential java class is a pair comparator,
Suggests to take a look at the Node object and write a new comparator in python.
'''
import numpy as np
import numpy.matlib
from buildDummyNodesAndLinks import buildDummyNodesAndLinks
from buildODmatrix import buildODmatrix
from cvn2tt import cvn2tt
from NodeModel import NodeModel
import math

#------------------file inport --------------------#

#scipy module is required to inport .mat matlab workspace file
import scipy.io

input_mat = scipy.io.loadmat('MS-DTA/small_case.mat')
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






nodes, links, ODmatrices = buildDummyNodesAndLinks(nodes, links, ODmatrices)
dt = 0.5
totT = round(20/dt)
timeSeries = np.arange(0.0,0.5*(ODmatrices.shape[1]),0.5)

ODmatrix,origins,destinations = buildODmatrix(ODmatrices,timeSeries,dt,totT)

from scipy.interpolate import interp1d


rc_dt = 10*dt
max_It = 1
rc_agg = "last"



def DTA_MSA(nodes, links,origins,destinations, ODmatrix, dt, totT, rc_dt, maxIt, rc_agg):
    from allOrNothingTF import allOrNothingTF

    #pass in all variables.
    '''
    Todo:
    semilogy graph plotting!
    '''
    #start_time = cputime <-- should I record this?

    if not maxIt: #<--unlikely becasue this input is compulsary.
        maxIt= 20

    #initialization
    totNodes = len(nodes.get('ID')) #<--row.
    totLinks = len(links.get('toNode'))
    totDest = len(destinations) #<--only 1 dimension, or len(destinations), if in form of a list.

    cvn_up = np.zeros((totLinks,totT+1, totDest))
    cvn_down = np.zeros((totLinks,totT+1, totDest))

    it = 0
    if(cvn_up.ndim>3):
        simTT = cvn2tt(np.sum(cvn_up,2), np.sum(cvn_up,2),dt,totT,links)
    else:
        simTT = cvn2tt(cvn_up, cvn_up,dt,totT,links)

    #simTT OK.
    import math
    gap_dt = math.inf

    TF = []#or numpy.zeros(0)

    TF_new, dummy1, dummy2 = allOrNothingTF(nodes,links,destinations,simTT,cvn_up,dt,totT,rc_dt,rc_agg)

#=======================NodeModel======================



    def LTM_MC(nodes, links, origins, destinaions,ODmatrix, dt, totT, TF):
        eps = np.finfo(float).eps
        totLinks = len(links.get('fromNode'))
        totDest = len(destinations)
        timeSlices = np.arange(0.0,totT+1,1)*0.5

        cvn_up = np.zeros((totLinks, totT+1, totDest))
        cvn_down = np.zeros((totLinks, totT+1, totDest))

        fromNodes= links.get('fromNode')
        toNodes = links.get('toNode')
        freeSpeeds = links.get('freeSpeed')
        capacities = links.get('capacity')
        kJams = links.get('KJam')
        lengths = links.get('length')
        wSpeeds = capacities/(kJams-capacities/freeSpeeds)

        originsAndDest = np.append(origins,destinations)
        normalNodes = np.setdiff1d(nodes.get('ID')-1,originsAndDest)
        #the problem is initialized ID as 1.2.3... not good.. so need subtract 1

        def loadOriginNodes(t):
            for o_index in range(0, len(origins)):
                o = origins[o_index]
                outgoingLinks = np.where(fromNodes==o)[0]
                for l_index in range(0, len(outgoingLinks)):
                    l = outgoingLinks[l_index]
                    for d_index in range(0,totDest):
                        SF_d = TF[o,t-1,d_index]*np.sum(ODmatrix[o_index, d_index, t-1])*dt
                        cvn_up[l,t,d_index]=cvn_up[l,t-1,d_index]+SF_d

        def loadDestinationNodes(t):
            for d_index in range(0, len(destinations)):
                d = destinations[d_index]
                incomingLinks = np.where(toNodes==d)[0]
                for l_index in range(0, len(incomingLinks)):
                    l=incomingLinks[l_index]
                    for d_index in range(0, totDest):
                        SF_d = findCVN(cvn_up[l,:,:],timeSlices[t]-lengths[l]/freeSpeeds[l],timeSlices,dt)-cvn_down[l, t-1,:]
                        cvn_down[l,t,:]=cvn_down[l,t-1,:]+SF_d

        def findCVN(cvn, time, timeSlices, dt):
            if time <= timeSlices[0]:
                val = cvn[0, 0, :]
            elif time >= timeSlices[-1]:
                val = cvn[0, -1, :]
            else:
                t1 = math.ceil(time / dt)
                t2 = t1 + 1
                val = cvn[t1-1] + (time/dt - t1 + 1) * (cvn[t2-1] - cvn[t1-1])
            return val

        def calculateDestSendFlow(l,t):

            SFCAP = capacities[l]*dt
            time = timeSlices[t]-lengths[l]/freeSpeeds[l]
            val = findCVN(cvn_up[l,:,:],time,timeSlices,dt)
            SF =val-cvn_down[l,t-1,:]
            if SF.all()>SFCAP:
                red = SFCAP/np.sum(SF)
                SF = np.dot(red,SF)
            return SF

        def calculateReceivingFlow_VQ(l):
            RF = capacities[l]*dt
            return RF

        def calculateReceivingFlow_HQ(l,t):
            RF = capacities[l]*dt
            val = np.sum(cvn_down[l,t-1,:])+kJams[l]*lengths[l]
            RF = min(RF,val-np.sum(cvn_up[l,t-1,:]))
            return RF
        def calculateReceivingFlow_FQ(l,t):
            RF = capacities[l]*dt
            time = timeSlices[t]-lengths[l]/wSpeeds[l]
            val = findCVN(np.sum(cvn_down[l,:,:],axis=1),time,timeSlices,dt)+kJams[l]*lengths[l]
            RF = min(RF,val-np.sum(cvn_up[l,t-1,:]))
            RF = max(RF,np.zeros(RF.shape))
            return RF
        def calculateTurningFractions(n,t):
            TF_n = np.zeros((nbIn, nbOut))
            if nbOut ==1:
                TF_n[0:nbIn,0]=1
            else:
                for d in range(0,totDest):
                    TF_n = TF_n+np.matlib.repmat(np.expand_dims(SF_d[:,d],axis=1),1,nbOut)*TF[n,t,d]

                TF_n = TF_n/np.matlib.repmat(np.expand_dims(np.finfo(float).eps+np.sum(TF_n,axis=1),axis=1),1,nbOut)
            return TF_n

        for t in range(1,totT+1):
            loadOriginNodes(t)

            for nIndex in range(0,len(normalNodes)):
                n = normalNodes[nIndex]
                incomingLinks = np.where(toNodes == n)[0]
                nbIn = len(incomingLinks)
                SF_d = np.zeros((nbIn, totDest))
                SF_tot = np.zeros((nbIn,1))
                SF = np.zeros((nbIn,1))

                for l_index in range(0, nbIn):
                    l = incomingLinks[l_index]
                    SF_d[l_index,:]=calculateDestSendFlow(l,t)
                    SF_tot[l_index]= np.sum(SF_d[l_index,:])
                    SF[l_index]=min(capacities[l]*dt,SF_tot[l_index])


                outgoingLinks = np.where(fromNodes==n)[0]
                nbOut = len(outgoingLinks)
                RF = np.zeros((nbOut,1))
                for l_index in range(0,nbOut):
                    l = outgoingLinks[l_index]
                    RF[l_index] = calculateReceivingFlow_FQ(l,t)

                TF_n = calculateTurningFractions(n,t-1)

                TransferFlow = NodeModel(nbIn, nbOut, SF,TF_n, RF, capacities[incomingLinks]*dt)

                red = np.sum(TransferFlow, axis=1)/(eps+SF_tot).transpose()
                for d in range(0, totDest):
                    cvn_down[incomingLinks,t,d]=cvn_down[incomingLinks,t-1,d]+red*SF_d[:,d]
                    cvn_up[outgoingLinks,t,d]=cvn_up[outgoingLinks,t-1,d]+np.dot((red*SF_d[:,d]),TF[n][t-1][d]).squeeze()


            loadDestinationNodes(t)


        return cvn_up, cvn_down

    while it<maxIt and gap_dt>0.000001:
        it = it+1
        if len(TF)==0:
            TF = TF_new
        else:
            for n in range(0,totNodes):
                for t in range(1,totT):
                    for d in range(1,totDest):
                        update = TF_new[n][t][d]-TF[n][t][d]
                        TF[n][t][d] = TF[n][t][d]-1/it*update

        cvn_up, cvn_down =LTM_MC(nodes,links, origins, destinations, ODmatrix, dt, totT, TF)

        simTT = cvn2tt(np.sum(cvn_up,axis=2),np.sum(cvn_down, axis=2), dt,totT, links)

        TF_new, gap_dt, gap_rc = allOrNothingTF(nodes, links, destinations, simTT, cvn_up, dt, totT, rc_dt, rc_agg)



#----after while------






a = DTA_MSA(nodes,links,origins,destinations,ODmatrix, dt, totT, rc_dt,max_It,rc_agg)


#[simTT] = cvn2tt(sum(cvn_up,3),sum(cvn_down,3),dt,totT,links);
