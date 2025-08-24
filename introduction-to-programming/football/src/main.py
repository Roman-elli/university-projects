import os
from game.game_setup import *
from game.game_state import *
from game.ball_moves import *

def main():
    match_state = init_state()
    
    os.makedirs('../data/game-record', exist_ok=True)
    os.makedirs('../data/game-results', exist_ok=True)
    os.makedirs('../data/game-titles', exist_ok=True)

    setup(match_state, True)
    while True:
        save_replay(match_state)
        match_state['window'].update()
        if match_state['ball'] is not None:
            ball_move(match_state)
        check_board_collisions(match_state)
        check_goal(match_state)
        if match_state['red_player'] is not None:
            check_blue_collisions(match_state)
        if match_state['blue_player'] is not None:
            check_red_collisions(match_state)

if __name__ == '__main__':
    main()