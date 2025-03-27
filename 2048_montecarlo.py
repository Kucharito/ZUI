import logic
import random
from concurrent.futures import ThreadPoolExecutor

mat = logic.start_game()
move_count = 0

moves = ["A", "S", "D"]
moves_with_w = ["A", "S", "D", "W"]


def evaluate_grid(grid):
    empty_cells = sum(row.count(0) for row in grid)
    max_tile = max(max(row) for row in grid)

    corner_bonus = 0
    corners = [(0, 0), (0, 3), (3, 0), (3, 3)]
    if any(grid[i][j] == max_tile for i, j in corners):
        corner_bonus = 20

    monotonicity_score = 0
    for row in grid:
        for i in range(3):
            if row[i] > row[i + 1]:
                monotonicity_score -= 1
            else:
                monotonicity_score += 1

    for col in zip(*grid):
        for i in range(3):
            if col[i] > col[i + 1]:
                monotonicity_score -= 1
            else:
                monotonicity_score += 1

    weight_matrix = [
        [4, 3, 2, 1],
        [5, 4, 3, 2],
        [6, 5, 4, 3],
        [7, 6, 5, 4],
    ]
    weighted_score = sum(grid[i][j] * weight_matrix[i][j] for i in range(4) for j in range(4))

    return empty_cells * 10 + corner_bonus + monotonicity_score + weighted_score / 100


def simulate_move(grid, move):
    if move == "A":
        return logic.move_left(grid)
    elif move == "S":
        return logic.move_down(grid)
    elif move == "D":
        return logic.move_right(grid)
    elif move == "W":
        return logic.move_up(grid)
    return grid, False, 0


def simulate_random_game(grid, depth=10):
    sim_grid = [row[:] for row in grid]
    sim_score = 0

    for _ in range(depth):
        legal_moves = [m for m in moves if simulate_move(sim_grid, m)[1]]
        if not legal_moves:
            break
        move = random.choice(legal_moves)
        sim_grid, changed, _ = simulate_move(sim_grid, move)
        if not changed:
            break
        sim_score += evaluate_grid(sim_grid)

    return sim_score


def monte_carlo_search(grid, simulations=100, depth=10):
    best_move = None
    best_score = -float('inf')

    with ThreadPoolExecutor() as executor:
        for move in moves:
            new_grid, changed, _ = simulate_move(grid, move)
            if not changed:
                continue

            futures = [executor.submit(simulate_random_game, [row[:] for row in new_grid], depth) for _ in range(simulations)]
            scores = [future.result() for future in futures]
            avg_score = sum(scores) / simulations

            if avg_score > best_score:
                best_score = avg_score
                best_move = move

    return best_move


while True:
    best_move = monte_carlo_search(mat, simulations=50, depth=20)

    if best_move is None:
        for move in moves_with_w:
            new_mat, changed, _ = simulate_move(mat, move)
            if changed:
                best_move = move
                break

    if best_move is None:
        break

    mat, _, _ = simulate_move(mat, best_move)
    move_count += 1

    status = logic.get_current_state(mat)
    print(f"Move {move_count}: {status}")
    for row in mat:
        print(row)

    if status != "GAME NOT OVER":
        break

    logic.add_new_2_or_4(mat)

print("\n\U0001F3C6 Hra skončila! \U0001F3C6")
print(f"Najvyššia dlaždica: {max(max(row) for row in mat)}")
print(f"Počet vykonaných ťahov: {move_count}")