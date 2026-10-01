def ReadSignalFile(file_name):
    expected_indices=[]
    expected_samples=[]
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline() # reads N
        line = f.readline() # read the index and value
        while line:
            L=line.strip()
            if len(L.split(' '))==2:
                L=line.split(' ')
                V1=int(L[0])
                V2=float(L[1])
                expected_indices.append(V1)
                expected_samples.append(V2)
                line = f.readline()
            else:
                break
    return expected_indices,expected_samples


def addSignals(indices1, samples1, indices2, samples2):
    result_indices = []
    result_samples = []
    
    # find the start and end of the new signal
    min_index = min(min(indices1), min(indices2))
    max_index = max(max(indices1), max(indices2))
    
    for i in range(min_index, max_index + 1):
        result_indices.append(i)
        
        # get value from the first signal (0 if not found)
        value1 = 0
        if i in indices1:
            position1 = indices1.index(i)
            value1 = samples1[position1]
            
        # get value from the second signal (0 if not found)
        value2 = 0
        if i in indices2:
            position2 = indices2.index(i)
            value2 = samples2[position2]
            
        # add the two values and save the result
        result_samples.append(value1 + value2)
        
    return result_indices, result_samples


def subtractSignals(indices1, samples1, indices2, samples2):
    # multiply the signal by -1
    inverse_indices2, inverse_samples2 = multiplySignalByConst(indices2, samples2, -1)
    
    # add the reverse signal to the other signal
    result_indices, result_samples = addSignals(indices1, samples1, inverse_indices2, inverse_samples2)
    
    return result_indices, result_samples


def multiplySignalByConst(indices, samples, constant):
    result_indices = []
    result_samples = []

    for i in range(len(indices)):
        result_indices.append(indices[i])

        value = samples[i]
        result_samples.append(value * constant)
        
    return result_indices, result_samples



def delay(indices, samples, constant): # shift right -> x(n-k)
    result_indices = []
    result_samples = []

    for i in range(len(indices)):
        value = samples[i]
        result_samples.append(value)

        new_index = indices[i] + constant
        result_indices.append(new_index)

    return result_indices, result_samples


def advance(indices, samples, constant): # shift left -> x(n+k)
    result_indices = []
    result_samples = []

    for i in range(len(indices)):
        value = samples[i]
        result_samples.append(value)

        new_index = indices[i] + (-1 * constant)
        result_indices.append(new_index)

    return result_indices, result_samples


def folding(indices, samples):
    result_indices = []
    result_samples = []

    result_samples = list(reversed(samples))
    indices = list(reversed(indices))

    for i in range(len(indices)):
        new_index = indices[i] * -1
        result_indices.append(new_index)

    return result_indices, result_samples