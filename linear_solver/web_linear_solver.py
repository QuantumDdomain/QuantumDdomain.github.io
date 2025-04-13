import numpy as np

def gauss_jordan_pivot(A, B):
    n = len(B)
    # Work on copies to avoid modifying originals
    A = A.copy()
    B = B.copy()

    for i in range(n):
        # Partial Pivoting: Swap rows if needed
        max_row = i
        for k in range(i + 1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        if A[max_row][i] == 0:
            raise ValueError("Matrix is singular or has no unique solution.")
        
        # Swap rows in both A and B
        if max_row != i:
            A[[i, max_row]] = A[[max_row, i]]
            B[i], B[max_row] = B[max_row], B[i]

        # Normalize the pivot row
        pivot = A[i][i]
        A[i] = A[i] / pivot
        B[i] = B[i] / pivot

        # Eliminate the current column from other rows
        for j in range(n):
            if j != i:
                factor = A[j][i]
                A[j] = A[j] - factor * A[i]
                B[j] = B[j] - factor * B[i]

    return B
