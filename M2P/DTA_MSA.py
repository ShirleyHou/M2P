import numpy as np
from scipy import sparse
from scipy.interpolate import interp1d

def DTA_MSA(nodes, links, origins, destinations, ODmatrix, dt, totT, rc_dt, maxIt, rc_agg):
    h = figure;

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
    totLinks = size_id.shape[0]
    totDest= destinations.shape[0] #<--only 1 dimension, or len(destinations), if in form of a list.

    cvn_up = np.zeros((totLinks,totT+1, totDest))
    cvn_down = np.zeros((totLinks,totT+1, totDest))

    it = 0


    '''
    build cvn2tt here!
    '''
    TF = []#or numpy.zeros(0)




def cvn2tt(cvn_up, cvn_down, dt, totT, links):
    simTT = np.zeros((links_id.shape[1],totT+1))

    timeSteps = dt*np.arrange(0,totT+1, 1)
    for l in range(0, links_id.shape[0]):
        down, iun = np.unique(cvn_down[l,:], return_index=True)
        if down.shape[0]<=1:
            simTT[l,:]=links_length[l]/links_freeSpeed[l]
        else:
            simTT[l,:]= interp1d(down,timeSteps[iun])(cvn_up[l,:])-dt*np.arrange(0,totT+1,1)
