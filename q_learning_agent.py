import logic
import random
import math

Q_table = {}

# ------------------- Stavová reprezentácia -------------------
def extract_state(grid):
    free = sum(row.count(0) for row in grid)
    max_tile = max(max(row) for row in grid)
    max_log = int(math.log2(max_tile)) if max_tile > 0 else 0
    in_corner = int(
        grid[0][0] == max_tile or grid[0][3] == max_tile or
        grid[3][0] == max_tile or grid[3][3] == max_tile
    )
    return (free, max_log, in_corner)

# ------------------- Výber akcie -------------------
def choose_action(state, epsilon):
    if random.random() < epsilon:
        return random.choice([0, 1, 2, 3])
    if state not in Q_table:
        Q_table[state] = [0, 0, 0, 0]
    return Q_table[state].index(max(Q_table[state]))

# ------------------- Aplikácia akcie -------------------
def apply_action(grid, action):
    if action == 0:
        new_grid, changed, reward = logic.move_left(grid)
    elif action == 1:
        new_grid, changed, reward = logic.move_right(grid)
    elif action == 2:
        new_grid, changed, reward = logic.move_up(grid)
    elif action == 3:
        new_grid, changed, reward = logic.move_down(grid)
    else:
        raise ValueError("Invalid action")
    return new_grid, reward, changed

# ------------------- Aktualizácia Q-tabule -------------------
def update_q_table(state, action, reward, next_state, alpha=0.5, gamma=0.95):
    if state not in Q_table:
        Q_table[state] = [0, 0, 0, 0]
    if next_state not in Q_table:
        Q_table[next_state] = [0, 0, 0, 0]
    max_next_q = max(Q_table[next_state])
    Q_table[state][action] += alpha * (reward + gamma * max_next_q - Q_table[state][action])

# ------------------- Parametre učenia -------------------
EPISODES = 10000
MAX_STEPS = 1000
epsilon = 1.0
min_epsilon = 0.1
epsilon_decay = 0.998
win_count = 0

# ------------------- Tréning -------------------
for episode in range(EPISODES):
    mat = logic.start_game()
    total_reward = 0

    for step in range(MAX_STEPS):
        state = extract_state(mat)
        action = choose_action(state, epsilon)
        new_grid, score, changed = apply_action(mat, action)

        if not changed:
            update_q_table(state, action, -5, state)
            continue

        logic.add_new_2_or_4(new_grid)
        next_state = extract_state(new_grid)

        free_cells = sum(row.count(0) for row in new_grid)
        max_tile = max(max(row) for row in new_grid)

        reward = score + free_cells * 5 + (int(math.log2(max_tile)) ** 2)
        if max_tile == 1024:
            reward += 200
        if max_tile >= 2048:
            reward += 1000
            win_count += 1
            update_q_table(state, action, reward, next_state)
            break

        update_q_table(state, action, reward, next_state)
        mat = new_grid
        total_reward += reward

        if logic.get_current_state(mat) == "LOST":
            break

    epsilon = max(min_epsilon, epsilon * epsilon_decay)

    if episode % 100 == 0:
        print(f"[{episode}] Total reward: {total_reward} | Epsilon: {epsilon:.3f} | Výhry: {win_count}")

# ------------------- Testovanie -------------------
print("\n🎯 Spúšťam testovanie agenta bez náhody...")
test_wins = 0
TEST_RUNS = 100

for _ in range(TEST_RUNS):
    mat = logic.start_game()
    for step in range(MAX_STEPS):
        state = extract_state(mat)
        action = choose_action(state, epsilon=0.0)
        new_grid, reward, changed = apply_action(mat, action)

        if not changed:
            break

        logic.add_new_2_or_4(new_grid)
        mat = new_grid

        if logic.get_current_state(mat) == "WON":
            test_wins += 1
            break
        elif logic.get_current_state(mat) == "LOST":
            break

print(f"\n✅ Výhry v testovacej fáze: {test_wins}/{TEST_RUNS}")
