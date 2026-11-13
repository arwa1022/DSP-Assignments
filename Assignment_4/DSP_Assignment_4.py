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


def moving_average(samples, window):
    result = []
    for i in range(len(samples) - window + 1):
        total = 0
        for j in range(window):
            total += samples[i + j]
        avg = total / window
        result.append(avg)
    return result


def first_derivative(samples):
    result = []
    for i in range(1, len(samples)):
        result.append(samples[i] - samples[i - 1])
    return result

def second_derivative(samples):
    result = []
    for i in range(1, len(samples) - 1):
        derivative = samples[i + 1] - 2 * samples[i] + samples[i - 1]
        result.append(derivative)
    return result


def convolution(h_indices, h_samples, x_indices, x_samples):
    result_indices = []
    result_samples = []

    min_index = h_indices[0] + x_indices[0]
    max_index = h_indices[-1] + x_indices[-1]

    x_dict = {x_indices[i]: x_samples[i] for i in range(len(x_indices))}

    for n in range(min_index, max_index + 1):
        total = 0
        for i in range(len(h_samples)):
            x_index = n - h_indices[i]
            if x_index in x_dict:
                total += h_samples[i] * x_dict[x_index]
                
        result_indices.append(n)
        result_samples.append(total)
    return result_indices, result_samples


def Compare_Signals(file_name, Your_indices, Your_samples):      
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
                
    if (len(expected_samples) != len(Your_samples)) or (len(expected_indices) != len(Your_indices)):
        print("Test case failed, your signal has a different length from the expected one")
        return
        
    for i in range(len(Your_indices)):
        if(Your_indices[i] != expected_indices[i]):
            print("Test case failed, your signal has different indicies from the expected one") 
            return
            
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Test case failed, your signal has different values from the expected one") 
            return
            
    print("Test case passed successfully")