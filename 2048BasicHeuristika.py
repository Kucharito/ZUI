import logic

# Spustenie hry
mat = logic.start_game()
move_count = 0
total_score =0
left_count=0
right_count=0
up_count=0
down_count=0

# Povolené pohyby (W len ako posledná možnosť)
moves = ["A", "S", "D"]
moves_with_w = ["A", "S", "D", "W"]


def evaluate_grid(grid):
    """
    Heuristická funkcia hodnotiaca stav mriežky:
    1. Počet voľných buniek (čím viac, tým lepšie).
    2. Najväčšia hodnota v rohu (preferujeme).
    3. Sú usporiadané veľké hodnoty vedľa seba?
    """
    empty_cells= sum(row.count(0) for row in grid)
    max_tile= max(max(row)for row in grid)

    corner_bonus=0
    if(grid[3][0] == max_tile or grid[3][3] == max_tile):
        corner_bonus=15

    # Penalizácia za rozhádzané čísla (chceme zoradenie)
    penalization=0
    for row in grid:
        for i in range(3):
            if(row[i]>=row[i+1]):
                penalization=penalization-2

    return empty_cells*5+corner_bonus+penalization


def simulate_move(grid, move):
    """Simuluje pohyb a vráti novú mriežku + či sa niečo zmenilo."""
    global left_count, right_count, up_count, down_count
    if move == "A":
        left_count=left_count+1
        return logic.move_left(grid)

    elif move == "S":
        down_count=down_count+1
        return logic.move_down(grid)

    elif move == "D":
        right_count = right_count + 1
        return logic.move_right(grid)

    elif move == "W":
        up_count = up_count + 1
        return logic.move_up(grid)

    return grid, False


def find_best_move(grid, depth):
    best_score = 0
    best_move=None

    for move in moves:
        new_grid,changed,score=simulate_move(grid,move)

        if (changed):
            score=score+evaluate_grid(new_grid)
            if(depth>1):
                _,next_score=find_best_move(new_grid,depth-1)
                score=score+next_score*0.8

            if(score>best_score):
                best_score=score
                best_move=move
    return best_move, best_score

while True:
    # Vybrať najlepší ťah
    best_move, _ = find_best_move(mat,5)
    if best_move is None:
        for move in moves_with_w:
            new_mat, changed, score = simulate_move(mat, move)
            if changed:
                best_move=move
                break

    if best_move is None:
        break

    mat, _, score= simulate_move(mat,best_move)
    move_count=move_count+1
    total_score=total_score+score

    # Skontrolovať stav hry
    status = logic.get_current_state(mat)
    print(f"Move {move_count}: {status}")

    # Vytlačiť aktuálnu hraciu plochu
    for row in mat:
        print(row)

    # Ak hra skončila, ukončíme cyklus
    if status != "GAME NOT OVER":
        break
    logic.add_new_2_or_4(mat)


print("\nHra skončila! ")
print(f"Najvyššia dlaždica: {max(max(row) for row in mat)}")
print(f"Počet vykonaných ťahov: {move_count}")
print(f"Celkové skóre: {total_score}")
print(f"Počet pohybov do lava: {left_count}")
print(f"Počet pohybov do prava: {right_count}")
print(f"Počet pohybov dole:{down_count}")
print(f"Počet pohybov hore:{up_count}")
