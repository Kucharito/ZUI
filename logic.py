import random

def start_game():
    mat = [[0] * 4 for _ in range(4)]
    add_new_2_or_4(mat)
    return mat

def add_new_2_or_4(mat):
    r, c = random.randint(0, 3), random.randint(0, 3)
    while mat[r][c] != 0:
        r, c = random.randint(0, 3), random.randint(0, 3)
    mat[r][c] = random.choices([2, 4], weights=[0.9, 0.1])[0]

def get_current_state(mat):
    for i in range(4):
        for j in range(4):
            if mat[i][j] == 2048:
                return 'WON'
    for i in range(4):
        for j in range(4):
            if mat[i][j] == 0:
                return 'GAME NOT OVER'
    for i in range(4):
        for j in range(3):
            if mat[i][j] == mat[i][j + 1] or mat[j][i] == mat[j + 1][i]:
                return 'GAME NOT OVER'
    return 'LOST'

def compress(mat):
    new_mat = [[0] * 4 for _ in range(4)]
    changed = False
    for i in range(4):
        pos = 0
        for j in range(4):
            if mat[i][j] != 0:
                new_mat[i][pos] = mat[i][j]
                if j != pos:
                    changed = True
                pos += 1
    return new_mat, changed

def merge(mat):
    changed = False
    score = 0
    for i in range(4):
        for j in range(3):
            if mat[i][j] == mat[i][j + 1] and mat[i][j] != 0:
                mat[i][j] *= 2
                mat[i][j + 1] = 0
                score += mat[i][j]
                changed = True
    return mat, changed, score

def reverse(mat):
    return [row[::-1] for row in mat]

def transpose(mat):
    return [list(row) for row in zip(*mat)]

def move_left(grid):
    new_grid, changed1 = compress(grid)
    new_grid, changed2, score = merge(new_grid)
    new_grid, _ = compress(new_grid)
    return new_grid, changed1 or changed2, score

def move_right(grid):
    new_grid = reverse(grid)
    new_grid, changed, score = move_left(new_grid)
    new_grid = reverse(new_grid)
    return new_grid, changed, score

def move_up(grid):
    new_grid = transpose(grid)
    new_grid, changed, score = move_left(new_grid)
    new_grid = transpose(new_grid)
    return new_grid, changed, score

def move_down(grid):
    new_grid = transpose(grid)
    new_grid, changed, score = move_right(new_grid)
    new_grid = transpose(new_grid)
    return new_grid, changed, score