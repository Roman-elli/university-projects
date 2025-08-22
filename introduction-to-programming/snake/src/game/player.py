
# Movement functions
def go_up(state):
    if state['snake']['current_direction'] != 'down':
        state['snake']['current_direction'] = 'up'

def go_down(state):
    if state['snake']['current_direction'] != 'up':
        state['snake']['current_direction'] = 'down'

def go_left(state):
    if state['snake']['current_direction'] != 'right':
        state['snake']['current_direction'] = 'left'

def go_right(state):
    if state['snake']['current_direction'] != 'left':
        state['snake']['current_direction'] = 'right'
