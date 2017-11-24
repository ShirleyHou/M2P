from scipy.sparse import lil_matrix
import numpy as np

def buildODmatrix(ODmatrices,timeSeries,dt,totT):

    #find all non empty od cells
    sumOD = ODmatrices[0,0];
    for i in range(0,ODmatrices.shape[1]):
        sumOD = sumOD + ODmatrices[0,i]

    origins = np.where(np.sum(sumOD,1)>0)[0] #row  index
    destinations = np.where(np.sum(sumOD,0)>0)[1] #col  index


    timeSteps = dt*np.arange(0,totT+0.5,1)

    '''
    python cannot have temporay mutable element, so have to keep a log of each iteration.
    od_matrix list will later be transfered into numpy array if needed.
    '''
    od_matrix = []

    for t in range(0,totT):
        sliceA = np.where(timeSeries<=timeSteps[t])[0] #<--smaller or equal to
        sliceA = sliceA[sliceA.size-1]

        sliceB = np.where(timeSeries<timeSteps[t+1])[0] #<--smaller
        sliceB = sliceB[sliceB.size-1]

        #tempSlices = np.asarray(np.unique(sliceA,sliceB)) #<--an array
        tempSlices = list(set([sliceA,sliceB]))# numpy unique does not work for filtering simple numbers.

        if(len(tempSlices)==1):

            temp_odmatrix = ODmatrices[0,min(ODmatrices.shape[1],tempSlices[0])][origins,:][:,destinations]

            od_matrix_cell = np.zeros((temp_odmatrix.shape[0],temp_odmatrix.shape[1]))
            for i in range(0, temp_odmatrix.shape[0]):
                for j in range (0,temp_odmatrix.shape[1]):
                    od_matrix_cell[i,j]=temp_odmatrix[i,j]

            od_matrix.append(od_matrix_cell)


        elif len(tempSlices)>1:
            '''be careful tempSlice is now a list, hasn't transferred to nparray yet'''
            #tempSlices = tempSlices[0]:tempSlices[len(tempSlices)]<-- whats the point of this line in Matlab?
            tempFrac = (timeSeries[tempSlices[1]]-timeSteps[t])/dt;
            temp_odmatrix = tempFrac*(ODmatrices[0, tempSlices[0]][origins,:][:,destinations])
            od_matrix_cell = np.zeros((temp_odmatrix.shape[0],temp_odmatrix.shape[1]))
            for i in range(temp_odmatrix.shape[0]):
                for j in range(temp_odmatrix.shape[1]):
                    od_matrix_cell[i,j]=temp_odmatrix[i,j]

            for kk in range(2,len(tempSlices)-1):

                tempFrac = (timeSeries[tempSlices[kk+1]]-timeSeries[tempSlices[kk]])/dt
                temp_odmatrix = tempFrac*(ODmatrices[0, tempSlices[-1]][origins,:][:,destinations])
                for i in range(temp_odmatrix.shape[0]):
                    for j in range(temp_odmatrix.shape[1]):
                        od_matrix_cell[i,j]=od_matrix_cell[i,j]+temp_odmatrix[i,j]

            tempFrac = (timeSteps[t+1]-timeSeries[tempSlices[-1]])/dt

            temp_odmatrix = tempFrac*ODmatrices[0,tempSlices[-1]][origins,:][:,destinations]

            for i in range(temp_odmatrix.shape[0]):
                for j in range(temp_odmatrix.shape[1]):
                    od_matrix_cell[i,j]=od_matrix_cell+temp_odmatrix[i,j]

            od_matrix.append(od_matrix_cell)


    od_matrix = np.asarray(od_matrix)
    #print(od_matrix.shape)
    od_matrix = np.moveaxis(od_matrix, 0, -1) #<--move the 1 axis to the 3nd to match style in matlab.
    return(od_matrix, origins, destinations)