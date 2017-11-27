'''
    return simTT
'''
import math
from scipy.interpolate import interp1d
import numpy as np
def cvn2tt(cvn_up, cvn_down, dt, totT, links):

    simTT = np.zeros((links.get('ID').shape[0],totT+1))#<--length of the links_id

    timeSteps = dt*np.arange(0,totT+1, 1)

    for l in range(0, links.get('ID').shape[0]):
        down, iun = np.unique(cvn_down[l,:], return_index=True)
        if down.shape[0]<=1:
            simTT[l,:]=links.get('length')[l]/links.get('freeSpeed')[l]
        else:
            f = interp1d(down,timeSteps[iun],bounds_error=False)
            interp = np.nan_to_num(f(cvn_up[l,:]))

            simTT[l,:]=np.maximum(interp-dt*np.arange(0,totT+1,1),links.get('length')[l]/links.get('freeSpeed')[l])
            simTT[l,cvn_up[l,:]-cvn_down[l,:]<10-3] = links.get('length')[l]/links.get('freeSpeed')[l]
            for t in range(1,totT+1):
                simTT[l,t]= np.maximum(simTT[l,t],simTT[l,t-1]-dt)

    return simTT
