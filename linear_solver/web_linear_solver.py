import numpy as np

def parse_input_matrix(text, n):
    rows = text.strip().split('\n')
    A = []
    for row in rows:
        numbers = list(map(float, row.strip().split()))
        if len(numbers) != n:
            raise ValueError("Each row of matrix A must have " + str(n) + " numbers.")
        A.append(numbers)
    return np.array(A, dtype=float)

def parse_input_vector(text, n):
    numbers = list(map(float, text.strip().split()))
    if len(numbers) != n:
        raise ValueError("Vector B must have exactly " + str(n) + " numbers.")
    return np.array(numbers, dtype=float)

def gauss_jordan_elimination(A, B):
    n = len(B)
    for i in range(n):
        max_row = i
        for j in range(i + 1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j

        if A[max_row][i] == 0:
            raise ValueError("Matrix is singular or has no unique solution.")

        # Swap rows in A and B
        A[[i, max_row]] = A[[max_row, i]]
        B[i], B[max_row] = B[max_row], B[i]

        # Make pivot element 1
        pivot = A[i][i]
        for j in range(n):
            A[i][j] /= pivot
        B[i] /= pivot

        # Eliminate all other elements in current column
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
                B[k] -= factor * B[i]

    return B
