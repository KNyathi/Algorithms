def diagonal_sort(mat):
    m = len(mat)
    if not (1 <= m <= 100):
        raise ValueError("Number of rows must be between 1 and 100 inclusive.")

    n = len(mat[0])
    if not (1 <= n <= 100):
        raise ValueError("Number of columns must be between 1 and 100 inclusive.")

    for row in mat:
        for val in row:
            if not (1 <= val <= 100):
                raise ValueError("Matrix element values must be between 1 and 100 inclusive.")

    # Helper function to sort diagonal starting at given position
    def sort_diagonal(i, j):
        diagonal = []
        while i < m and j < n:
            diagonal.append(mat[i][j])
            i += 1
            j += 1
        diagonal.sort()
        i, j = i - 1, j - 1  # Move back to the last element of the diagonal
        while diagonal:
            mat[i][j] = diagonal.pop()
            i -= 1
            j -= 1

    # Sort diagonals starting from the first row
    for j in range(n):
        sort_diagonal(0, j)

    # Sort diagonals starting from the first column
    for i in range(1, m):
        sort_diagonal(i, 0)

    return mat

# Examples
mat1 = [[3, 3, 1, 1], [2, 2, 1, 2], [1, 1, 1, 2]]
print(diagonal_sort(mat1))

mat2 = [[11, 25, 66, 1, 69, 7], [23, 55, 17, 45, 15, 52], [75, 31, 36, 44, 58, 8], [22, 27, 33, 25, 68, 4], [84, 28, 14, 11, 5, 50]]
print(diagonal_sort(mat2))

invalid_rows = [[1] * 101 for _ in range(101)]
try:
    diagonal_sort(invalid_rows)
except ValueError as e:
    print("Error:", e)