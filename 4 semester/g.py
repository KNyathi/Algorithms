def is_safe(board, row, col):
    # Check if there is a queen in the same column
    for i in range(row):
        if board[i][col] == 1:
            return False

    # Check upper left diagonal
    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == 1:
            return False

    # Check upper right diagonal
    for i, j in zip(range(row, -1, -1), range(col, len(board))):
        if board[i][j] == 1:
            return False

    return True

def solve_queens(board, row, solutions):
    if row >= len(board):
        solutions.append([row[:] for row in board])
        return

    for col in range(len(board)):
        if is_safe(board, row, col):
            board[row][col] = 1
            solve_queens(board, row + 1, solutions)
            board[row][col] = 0

def print_board(board):
    for row in board:
        print(" ".join(map(str, row)))

def find_solutions():
    solutions = []
    board = [[0 for _ in range(8)] for _ in range(8)]
    solve_queens(board, 0, solutions)
    return solutions

all_solutions = find_solutions()
if all_solutions:
    print("Number of solutions found:", len(all_solutions))
    for i, solution in enumerate(all_solutions):
        print("Solution", i+1)
        print_board(solution)
        print()
else:
    print("No solutions found.")