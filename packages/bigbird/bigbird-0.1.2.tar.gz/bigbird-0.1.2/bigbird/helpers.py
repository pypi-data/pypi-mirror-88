def randomize(matrix):
    inputs = len(matrix[0])
    outputs = len(matrix)
    for i in range(outputs):
        for j in range(inputs):
            matrix[i][j] = xav(inputs)

    return matrix

def sig(x):
    return 1 / (1 + np.exp(-4.9 * x))

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)

def xav(i):
    return np.random.normal(0, 1/np.sqrt(i), 1)[0]
