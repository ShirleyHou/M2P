import numpy as np
import numpy.matlib

def NodeModel(nbIncomingLinks, nbOutgoingLinks, sendingFlow, turningFractions, receivingFlow, incomingLinks_capacity):
    adjustedReceivingFlow = receivingFlow
    competingLinks = numpy.matlib.repmat(sendingFlow > 0, 1, nbOutgoingLinks)
    competingLinks[turningFractions == 0] = 0
    activeOutLinks = np.any(competingLinks, axis=0)
    distrFactors = turningFractions * np.matlib.repmat(np.expand_dims(incomingLinks_capacity, axis=1), 1,
                                                       nbOutgoingLinks)
    TurnFlows = np.zeros((nbIncomingLinks, nbOutgoingLinks))

    while np.any(activeOutLinks):
        alpha = adjustedReceivingFlow / np.expand_dims(np.sum(distrFactors * competingLinks, axis=0), axis=1)
        alpha[~activeOutLinks] = np.inf
        alpha_min = np.amin(alpha)
        j = np.argmin(alpha)
        if np.any(sendingFlow[competingLinks[:, j]]<= np.expand_dims(np.dot(alpha_min, incomingLinks_capacity[competingLinks[:, j]]),axis=1)):
            for a in range(0, nbIncomingLinks):
                if competingLinks[a, j]:
                    if sendingFlow[a] <= np.dot(alpha_min,incomingLinks_capacity[a]):
                        for b in range(0, nbOutgoingLinks):
                            if activeOutLinks[b]:
                                TurnFlows[a, b] = np.dot(turningFractions[a, b], sendingFlow[a])
                                adjustedReceivingFlow[b] = adjustedReceivingFlow[b] - TurnFlows[a, b]
                                competingLinks[a, b] = False
                                if np.all(~competingLinks[:, b]):
                                    activeOutLinks[b] = False

        else:
            for a in range(0, nbIncomingLinks):
                if competingLinks[a, j]:
                    for b in range(0, nbOutgoingLinks):
                        if activeOutLinks[b]:
                            TurnFlows[a, b] = np.dot(alpha_min,distrFactors[a, b])
                            adjustedReceivingFlow[b] = adjustedReceivingFlow[b] - TurnFlows[a, b]
                            competingLinks[a, b] = False
                            if np.all(~competingLinks[:, b]):
                                activeOutLinks[b] = False

            activeOutLinks[j] = False
    return TurnFlows