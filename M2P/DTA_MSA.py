from LTM_MC import LTM_MC
import numpy as np
from cvn2tt import cvn2tt

def DTA_MSA(nodes, links,origins,destinations, ODmatrix, dt, totT, rc_dt, maxIt, rc_agg):
    from allOrNothingTF import allOrNothingTF

    #pass in all variables.
    '''
    Todo:
    semilogy graph plotting!
    '''
    import time
    start_time = time.clock()

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


    import matplotlib.pyplot as plt
    plt.figure()
    count = 0
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


        '''
        TODO: plot
        
        '''
        timecount = time.clock()-start_time
        a = plt.semilogy(timecount,gap_dt,'r.',label='gap based on simulation interval' )
        b = plt.semilogy(timecount,gap_rc, 'ob',mfc='none',label= 'gap based on route choice interval')

        if(count==0):
            plt.legend()

        plt.pause(0.01)
        count=count+1

        #print("Plotting here")

    if it>maxIt:
        print("Maximum Iteration limit reached: ", maxIt, "Gap: ", gap_dt)
    else:
        print("Convergence reached in iteration ", it, "Gap: ", gap_dt)

    return cvn_up, cvn_down, TF
#----after while------