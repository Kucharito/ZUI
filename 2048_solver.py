import logic

# Spustenie hry
mat = logic.start_game()
move_count = 0
total_score = 0
left_count = 0
right_count = 0
up_count = 0
down_count = 0

def evaluate_grid(grid):
    """
    Vylepšená heuristika:
      - Počet voľných buniek (čím viac, tým lepšie)
      - Najväčšia dlaždica v rohu (prioritizované)
      - Monotonicita (čísla zoradené správnym smerom)
      - Smoothness (menej veľkých rozdielov medzi dlaždicami)
      - Priorita na zlúčenie dlaždíc
    """
    free_cells = sum(row.count(0) for row in grid)
    max_tile = max(max(row) for row in grid)

    # Bonus za umiestnenie najväčšej dlaždice v rohu
    corner_bonus = 0
    if grid[3][0] == max_tile or grid[3][3] == max_tile:
        corner_bonus = 500  # Zvýšený bonus

    # Monotonicita – preferujeme, ak sú hodnoty zoradené
    monotonicity = 0
    for row in grid:
        for i in range(3):
            if row[i] >= row[i + 1]:
                monotonicity += 2
            else:
                monotonicity -= 2

    # Smoothness: penalizácia za veľké rozdiely medzi susednými dlaždicami
    smoothness = 0
    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                for di, dj in [(1, 0), (0, 1)]:
                    ni, nj = i + di, j + dj
                    if ni < 4 and nj < 4 and grid[ni][nj] != 0:
                        smoothness -= abs(grid[i][j] - grid[ni][nj])

    # Bonus za počet možných zlúčení
    merge_bonus = 0
    for i in range(4):
        for j in range(3):
            if grid[i][j] == grid[i][j + 1]:  # Horizontálne zlúčenie
                merge_bonus += grid[i][j] * 2
            if grid[j][i] == grid[j + 1][i]:  # Vertikálne zlúčenie
                merge_bonus += grid[j][i] * 2

    return free_cells * 10 + corner_bonus + monotonicity * 3 + smoothness * 0.1 + merge_bonus

def simulate_move(grid, move):
    """Simuluje daný pohyb a vráti novú mriežku spolu s príznakom, či sa zmenila a skóre."""
    global left_count, right_count, up_count, down_count
    if move == "A":
        return logic.move_left(grid)
    elif move == "S":
        return logic.move_down(grid)
    elif move == "D":
        return logic.move_right(grid)
    elif move == "W":
        return logic.move_up(grid)
    return grid, False, 0

def expectimax(grid, depth, is_chance):
    """
    Expectimax algoritmus so správnym generovaním "2" a "4":
      - Ak je depth 0, vrátime heuristické hodnotenie.
      - V hráčovej vrstve (is_chance == False) vyberieme ťah, ktorý maximalizuje očakávanú hodnotu.
      - V náhodnej vrstve (is_chance == True) generujeme "2" (90%) a "4" (10%) a spriemerujeme výsledky.
    """
    state = logic.get_current_state(grid)
    if state == "WON":
        return 1000000
    if state == "LOST":
        return -1000000
    if depth == 0:
        return evaluate_grid(grid)

    if not is_chance:
        best_value = -float('inf')
        for move in ["A", "S", "D", "W"]:
            new_grid, changed, _ = simulate_move(grid, move)
            if not changed:
                continue
            value = expectimax(new_grid, depth - 1, True)
            best_value = max(best_value, value)
        return best_value if best_value != -float('inf') else evaluate_grid(grid)
    else:
        empty_cells = [(i, j) for i in range(4) for j in range(4) if grid[i][j] == 0]
        if not empty_cells:
            return evaluate_grid(grid)

        total_value = 0
        for (i, j) in empty_cells:
            new_grid_2 = [row[:] for row in grid]
            new_grid_4 = [row[:] for row in grid]

            new_grid_2[i][j] = 2
            new_grid_4[i][j] = 4

            total_value += 0.9 * expectimax(new_grid_2, depth - 1, False)
            total_value += 0.1 * expectimax(new_grid_4, depth - 1, False)

        return total_value / len(empty_cells)

def find_best_move(grid, depth):
    best_move = None
    best_value = -float('inf')
    for move in ["A", "S", "D", "W"]:
        new_grid, changed, _ = simulate_move(grid, move)
        if not changed:
            continue
        value = expectimax(new_grid, depth, True)
        if value > best_value:
            best_value = value
            best_move = move
    return best_move

# Hlavná slučka hry
while True:
    # Vyberieme najlepší ťah pomocou Expectimaxu s vyššou hĺbkou
    best_move = find_best_move(mat, 4)

    if best_move is None:
        break

    mat, changed, score = simulate_move(mat, best_move)
    if changed:
        move_count += 1
        total_score += score
        if best_move == "A":
            left_count += 1
        elif best_move == "S":
            down_count += 1
        elif best_move == "D":
            right_count += 1
        elif best_move == "W":
            up_count += 1

    status = logic.get_current_state(mat)
    print(f"Move {move_count}: {status}")
    for row in mat:
        print(row)

    if status != "GAME NOT OVER":
        break

    logic.add_new_2_or_4(mat)

print("\nHra skončila!")
print(f"Najvyššia dlaždica: {max(max(row) for row in mat)}")
print(f"Počet vykonaných ťahov: {move_count}")
print(f"Celkové skóre: {total_score}")
print(f"Počet pohybov do lava: {left_count}")
print(f"Počet pohybov do prava: {right_count}")
print(f"Počet pohybov hore :{up_count}")
print(f"Počet pohybov dole: {down_count}")