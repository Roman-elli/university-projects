import os

from utils.file import write_high_score_to_file
from game.game_setup import *
from game.game_state import *
from game.snake_move import *

def main():
    state = init_state()
    os.makedirs('../data', exist_ok=True)
    setup(state)
    while not check_collisions(state):
        state['window'].update()
        check_if_food_to_eat(state)
        move_head(state)
        move_body(state)
        time.sleep(SPEED)
    print("YOU LOSE!")
    create_lose_board(state)
    if state['new_high_score']:
        write_high_score_to_file(state)

if __name__ == "__main__":
    main()