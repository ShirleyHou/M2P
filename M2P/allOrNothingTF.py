import numpy as np
from scipy.sparse import coo_matrix
from dijkstra import dijkstra
def allOrNothingTF(nodes, links, destinations, simTT, cvn_up, dt, totT, rc_dt, rc_agg):
    totNodes = len(nodes.get('ID'))
    totLinks = len(links.get('ID'))
    totDest = len(destinations)

    strN = links.get('fromNode')
    endN = links.get('toNode')

    if (cvn_up.shape[0] == 0):
        cvn_up = np.zeros((totLinks, totT + 1, totDest))

    TF = [[[1 for i in range(totDest)] for j in range(totT)] for k in range(nodes.get('ID').shape[0])]
    # TF = [[[1]*totDest]*totT]*nodes.get('ID').shape[0] #<--now TF is a 43*40*5 empty cell.
    # print(np.asarray(TF).shape)

    timeSteps = dt * np.arange(0, totT + 1, 1)
    timeRC = rc_dt * np.arange(0, totT + 1, 1)
    timeRC = np.delete(timeRC, np.where(timeRC > timeSteps[-1]))

    gap = np.zeros((totLinks, totT + 1))
    gap_dt = 0
    gap_rc = 0
    act_t = np.zeros(totT + 1, dtype=bool)  # size = (41,)
    gVeh = np.floor(rc_dt / dt)

    def arr_map_d(d_index):

        d = destinations[d_index]

        netCostMatrix = coo_matrix((simTT[:, -1], (endN, strN)), shape=(totNodes, totNodes))

        par, dist, path = dijkstra(netCostMatrix, d)
        # par & dist: 43*1



        parent = np.zeros((totNodes, totT + 1))
        parent[:, totT] = par

        arr_map = np.zeros((totNodes, totT + 1))

        arr_map[:, totT] = dist + dt * totT

        import math
        for t in range(totT, -1, -1):
            for n in range(0, totNodes):
                if np.any(n==destinations):
                    if n != d:
                        arr_map[n, t] = math.inf
                    else:
                        arr_map[n, t] = (t-1) * dt
                    continue
                outgoinglinks = np.where(strN == n)[0]
                arr = math.inf

                for l in outgoinglinks:  # np array is also iterable

                    time = timeSteps[t] + simTT[l, t]

                    if time >= timeSteps[-1]:
                        val = time - dt * totT + arr_map[endN[l], -1]
                    else:
                        t1 = np.minimum(totT + 1, 1 + np.maximum(t + 1, 1 + math.floor(time / dt))) - 1
                        t2 = np.minimum(totT + 1, t1 + 1) - 1
                        val = arr_map[endN[l], t1] + np.maximum(0, (1 + time / dt - t1)) * (
                        arr_map[endN[l], t2] - arr_map[endN[l], t1])

                    if cvn_up[l, t, d_index] > 0:
                        gap[l, t] = gap[l, t] + val
                    if val <= arr:
                        arr = val
                        parent[n, t] = endN[l]

                for l in outgoinglinks:
                    if cvn_up[l, t, d_index] > 0:
                        gap[l, t] = gap[l, t] - arr

                arr_map[n, t] = arr

        return arr_map, parent
        # =====end of arr_map_d====================

    if rc_agg == "first":
        timeVeh = 0

    elif rc_agg == "middle":
        timeVeh = rc_dt / 2

    elif rc_agg == "last":
        timeVeh = rc_dt

    elif rc_agg == '':

        for d_index in range(0, totDest):
            arr_map_d(d_index)
        TF = np.asarray([])
        return TF, gap_dt, gap_rc

    elif rc_agg == 'inst':
        for d_index in range(0, totDest):

            d = destinations[d_index]
            netCostMatrix = coo_matrix((simTT[:, -1], (endN, strN)), (totNodes, totNodes))
            parent, distance, path = dijkstra(netCostMatrix, d)

            for n in range(0, totNodes):
                incomingLinks = np.where(endN == n)[0]  # <--an array. If its [0][0] its element at one particular index
                outgoingLinks = np.where(strN == n)[0]

                # remember TF is a list
                TF[n][0][d_index] = np.zeros[max(1, incomingLinks.shape[0]), outgoingLinks.shape[0]]

            gap = []
        return TF, gap_dt, gap_rc

    tVeh = np.floor(timeVeh / dt)

    for d_index in range(0, totDest):
        arr_map, parent = arr_map_d(d_index)

        for n in range(0, totNodes):
            next_rc = 1
            incomingLinks = np.where(endN == n)[0]
            outgoingLinks = np.where(strN == n)[0]

            if len(outgoingLinks) <= 1:
                for t in range(0, totT):
                    TF[n][t][d_index] = np.ones((max(1, len(incomingLinks)), max(1, len(outgoingLinks))))

            else:
                # par = np.zeros((1))
                for t in range(0, totT):
                    a = timeRC[np.minimum(len(timeRC), next_rc)-1]

                    if timeSteps[t] >= a:
                        next_rc = next_rc + 1

                        par = parent[n, int(min(totT+1, t + tVeh))]
                        act_t[int(min(totT+1, t + tVeh))] = True

                    TF[n][t][d_index] = np.zeros((max(1, len(incomingLinks)), len(outgoingLinks)))

                    TF[n][t][d_index][:, endN[outgoingLinks]==par] = 1

        gap_dt = gap_dt + np.sum(np.sum(gap[:, 1:] * np.diff(cvn_up[:, :, d_index], n=1, axis=1)))

        # print(np.where(act_t != 0)[0]+ gVeh - tVeh)
        new_index = np.zeros(len(np.where(act_t != 0)[0] + gVeh - tVeh) + 1)
        new_index[1:] = np.where(act_t != 0)[0] + gVeh - tVeh

        gap_rc = gap_rc + np.sum(
            np.sum(gap[:, act_t] * np.diff(cvn_up[:, new_index.astype(int), d_index], n=1, axis=1)))

    return np.asarray(TF), gap_dt, gap_rc
