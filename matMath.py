# Operaciones con matrices obtenidas de varias fuentes

# https://stackoverflow.com/questions/40120892/creating-a-matrix-in-python-without-numpy
def createMatrix(rowCount, colCount, dataList):
    mat = []
    for i in range(rowCount):
        rowList = []
        for j in range(colCount):
            # you need to increment through dataList here, like this:
            rowList.append(dataList[rowCount * i + j])
        mat.append(rowList)

    return mat


# https://stackoverflow.com/questions/28253102/python-3-multiply-a-vector-by-a-matrix-without-numpy
def multMatrix(v, G):
    result = [[0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0]]
    for i in range(len(G[0])):  # this loops through columns of the matrix
        total = 0
        for j in range(len(v)):  # this loops through vector coordinates & rows of matrix
            for k in range(len(v)):
                result[i][j] += v[i][k] * G[k][j]
    return result


# Function to print identity matrix
# https://www.geeksforgeeks.org/python-program-for-identity-matrix/
def identityMatrix(size):
    matrix = []
    for row in range(0, size):
        matrix.append([])
        for col in range(0, size):
            # Here end is used to stay in same line. Append instead of print
            if (row == col):
                matrix[row].append(1)
                #print("1 ", end=" ")
            else:
                matrix[row].append(0)
                #print("0 ", end=" ")
    return matrix


# https://stackoverflow.com/questions/35208160/dot-product-in-python-without-numpy
def dotMatrix(v1, v2):
    return sum([x*y for x, y in zip(v1, v2)])


# Simplemente multiplicar vectores
def vectMultMatrix(M, v):
    return [dotMatrix(r, v) for r in M]
