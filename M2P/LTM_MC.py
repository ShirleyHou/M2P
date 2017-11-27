from NodeModel import NodeModel
import numpy as np
import math
def LTM_MC(nodes, links, origins, destinations, ODmatrix, dt, totT, TF):
    eps = np.finfo(float).eps
    totLinks = len(links.get('fromNode'))
    totDest = len(destinations)
    timeSlices = np.arange(0.0, totT + 1, 1) * 0.5

    cvn_up = np.zeros((totLinks, totT + 1, totDest))
    cvn_down = np.zeros((totLinks, totT + 1, totDest))

    fromNodes = links.get('fromNode')
    toNodes = links.get('toNode')
    freeSpeeds = links.get('freeSpeed')
    capacities = links.get('capacity')
    kJams = links.get('KJam')
    lengths = links.get('length')
    wSpeeds = capacities / (kJams - capacities / freeSpeeds)

    originsAndDest = np.append(origins, destinations)
    normalNodes = np.setdiff1d(nodes.get('ID') - 1, originsAndDest)

    # the problem is initialized ID as 1.2.3... not good.. so need subtract 1

    def loadOriginNodes(t):
        for o_index in range(0, len(origins)):
            o = origins[o_index]
            outgoingLinks = np.where(fromNodes == o)[0]
            for l_index in range(0, len(outgoingLinks)):
                l = outgoingLinks[l_index]
                for d_index in range(0, totDest):
                    SF_d = TF[o, t - 1, d_index] * np.sum(ODmatrix[o_index, d_index, t - 1]) * dt
                    cvn_up[l, t, d_index] = cvn_up[l, t - 1, d_index] + SF_d

    def loadDestinationNodes(t):
        for d_index in range(0, len(destinations)):
            d = destinations[d_index]
            incomingLinks = np.where(toNodes == d)[0]
            for l_index in range(0, len(incomingLinks)):
                l = incomingLinks[l_index]
                for d_index in range(0, totDest):
                    SF_d = findCVN(cvn_up[l, :, :], timeSlices[t] - lengths[l] / freeSpeeds[l], timeSlices,
                                   dt) - cvn_down[l, t - 1, :]
                    cvn_down[l, t, :] = cvn_down[l, t - 1, :] + SF_d

    def findCVN(cvn, time, timeSlices, dt):
        if time <= timeSlices[0]:
            val = cvn[0, 0, :]
        elif time >= timeSlices[-1]:
            val = cvn[0, -1, :]
        else:
            t1 = math.ceil(time / dt)
            t2 = t1 + 1
            val = cvn[t1 - 1] + (time / dt - t1 + 1) * (cvn[t2 - 1] - cvn[t1 - 1])
        return val

    def calculateDestSendFlow(l, t):

        SFCAP = capacities[l] * dt
        time = timeSlices[t] - lengths[l] / freeSpeeds[l]
        val = findCVN(cvn_up[l, :, :], time, timeSlices, dt)
        SF = val - cvn_down[l, t - 1, :]
        if SF.all() > SFCAP:
            red = SFCAP / np.sum(SF)
            SF = np.dot(red, SF)
        return SF

    def calculateReceivingFlow_VQ(l):
        RF = capacities[l] * dt
        return RF

    def calculateReceivingFlow_HQ(l, t):
        RF = capacities[l] * dt
        val = np.sum(cvn_down[l, t - 1, :]) + kJams[l] * lengths[l]
        RF = min(RF, val - np.sum(cvn_up[l, t - 1, :]))
        return RF

    def calculateReceivingFlow_FQ(l, t):
        RF = capacities[l] * dt
        time = timeSlices[t] - lengths[l] / wSpeeds[l]
        val = findCVN(np.sum(cvn_down[l, :, :], axis=1), time, timeSlices, dt) + kJams[l] * lengths[l]
        RF = min(RF, val - np.sum(cvn_up[l, t - 1, :]))
        RF = max(RF, np.zeros(RF.shape))
        return RF

    def calculateTurningFractions(n, t):
        TF_n = np.zeros((nbIn, nbOut))
        if nbOut == 1:
            TF_n[0:nbIn, 0] = 1
        else:
            for d in range(0, totDest):
                TF_n = TF_n + np.matlib.repmat(np.expand_dims(SF_d[:, d], axis=1), 1, nbOut) * TF[n, t, d]

            TF_n = TF_n / np.matlib.repmat(np.expand_dims(np.finfo(float).eps + np.sum(TF_n, axis=1), axis=1), 1, nbOut)
        return TF_n

    for t in range(1, totT + 1):
        loadOriginNodes(t)

        for nIndex in range(0, len(normalNodes)):
            n = normalNodes[nIndex]
            incomingLinks = np.where(toNodes == n)[0]
            nbIn = len(incomingLinks)
            SF_d = np.zeros((nbIn, totDest))
            SF_tot = np.zeros((nbIn, 1))
            SF = np.zeros((nbIn, 1))

            for l_index in range(0, nbIn):
                l = incomingLinks[l_index]
                SF_d[l_index, :] = calculateDestSendFlow(l, t)
                SF_tot[l_index] = np.sum(SF_d[l_index, :])
                SF[l_index] = min(capacities[l] * dt, SF_tot[l_index])

            outgoingLinks = np.where(fromNodes == n)[0]
            nbOut = len(outgoingLinks)
            RF = np.zeros((nbOut, 1))
            for l_index in range(0, nbOut):
                l = outgoingLinks[l_index]
                RF[l_index] = calculateReceivingFlow_FQ(l, t)

            TF_n = calculateTurningFractions(n, t - 1)

            TransferFlow = NodeModel(nbIn, nbOut, SF, TF_n, RF, capacities[incomingLinks] * dt)

            red = np.sum(TransferFlow, axis=1) / (eps + SF_tot).transpose()
            for d in range(0, totDest):
                cvn_down[incomingLinks, t, d] = cvn_down[incomingLinks, t - 1, d] + red * SF_d[:, d]
                cvn_up[outgoingLinks, t, d] = cvn_up[outgoingLinks, t - 1, d] + np.dot((red * SF_d[:, d]),
                                                                                       TF[n][t - 1][d]).squeeze()

        loadDestinationNodes(t)

    return cvn_up, cvn_down