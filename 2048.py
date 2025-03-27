import logic
import random

if __name__ == '__main__':
    mat = logic.start_game()
    highest_score = 0

    directions = ['W', 'A', 'S', 'D']

    for step in range(1000):
        x = random.choice(directions)

        # Vykonaj pohyb a zisti, či sa niečo zmenilo
        if x == 'W':
            mat, changed, score = logic.move_up(mat)
        elif x == 'S':
            mat, changed, score = logic.move_down(mat)
        elif x == 'A':
            mat, changed, score = logic.move_left(mat)
        elif x == 'D':
            mat, changed, score = logic.move_right(mat)

        if not changed:
            continue

        highest_score += score

        logic.add_new_2_or_4(mat)

        status = logic.get_current_state(mat)
        print(status)

        for row in mat:
            print(row)

        print("Step:", step)
        print("Highest Score:", highest_score)

        if status != 'GAME NOT OVER':
            break

    print("Hra skoncila")
