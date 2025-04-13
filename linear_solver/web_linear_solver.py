import numpy as np

def parse_input_matrix(text, n):
    lines = text.strip().splitlines()
    A = np.zeros((n, n))
    for i in range(n):
        A[i] = list(map(float, lines[i].strip().split()))
    return A

def parse_input_vector(text, n):
    return np.array(list(map(float, text.strip().split())), dtype=float)

def gauss_jordan_elimination(A, B):
    n = len(B)
    A = A.copy()
    B = B.copy()

    for i in range(n):
        # Partial pivoting
        max_row = i
        for k in range(i + 1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k

        if A[max_row][i] == 0:
            raise ValueError("Matrix is singular or no unique solution exists.")

        # Swap rows in A and B
        A[[i, max_row]] = A[[max_row, i]]
        B[i], B[max_row] = B[max_row], B[i]

        # Normalize pivot row
        pivot = A[i][i]
        for j in range(n):
            A[i][j] /= pivot
        B[i] /= pivot

        # Eliminate other rows
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
                B[k] -= factor * B[i]

    return B
