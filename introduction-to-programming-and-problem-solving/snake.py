import time
from random import randint
import functools
import turtle

MAX_X = 600
MAX_Y = 640
DEFAULT_SIZE = 20
SNAKE_SHAPE = 'square'
HIGH_SCORES_FILE_PATH = 'snake-game/data/high_scores.txt'
SPEED = 0.12

# Load high score from file into state
def load_high_score(state):
    with open(HIGH_SCORES_FILE_PATH, "a") as statehs:
        statehs.close()
    with open(HIGH_SCORES_FILE_PATH, "r") as statehs:
        empty = statehs.read(1)
        if not empty:
            state["high_score"] = 0
        else:
            state["high_score"] = int(statehs.readlines()[-1])
        statehs.close()

# Write high score to file if beaten
def write_high_score_to_file(state):
    with open(HIGH_SCORES_FILE_PATH, "a+") as statehs:
        print("NEW HIGHSCORE!!!")
        statehs.write("\n")
        statehs.write(str(state["high_score"]))
        statehs.close()

# Create and display score board
def create_score_board(state):
    score_board = turtle.Turtle()
    score_board.speed(0)
    score_board.shape("square")
    score_board.color("chocolate3")
    score_board.penup()
    score_board.hideturtle()
    score_board.goto(0, MAX_Y / 2.3)
    state['score_board'] = score_board
    load_high_score(state)
    update_score_board(state)

# Display message when losing
def create_lose_board(state):
    lose = turtle.Turtle()
    lose.speed(0)
    lose.shape("square")
    lose.color("chocolate3")
    lose.penup()
    lose.hideturtle()
    lose.goto(0, 0)
    if state["new_high_score"]:
        lose.write("NEW HIGHSCORE!! CONGRATULATIONS!!", align="center", font=("Comic Sans MS", 15, "normal"))
    else:
        lose.write("YOU LOSE ! ! !", align="center", font=("Comic Sans MS", 15, "normal"))
    time.sleep(2)

# Update score board display
def update_score_board(state):
    state['score_board'].clear()
    if state["score"] >= state["high_score"]:
        state["score_board"].color("gold")
    state['score_board'].write(
        "Score: {} High Score: {}".format(state['score'], state['high_score']), 
        align="center", font=("Comic Sans MS", 24, "normal")
    )

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

# Initialize game state
def init_state():
    state = {'score_board': None, 'new_high_score': False, 'high_score': 0, 'score': 0, 'food': None, 'window': None, "player": ""}
    snake = {'head': None, 'current_direction': None}
    state['snake'] = snake
    return state

# Setup window, snake, score and food
def setup(state):
    window = turtle.Screen()
    window.setup(width=MAX_X, height=MAX_Y)
    window.listen()
    window.onkey(functools.partial(go_up, state), 'w')
    window.onkey(functools.partial(go_down, state), 's')
    window.onkey(functools.partial(go_left, state), 'a')
    window.onkey(functools.partial(go_right, state), 'd')
    window.tracer(0)

    background(state)
    snake = state['snake']
    snake['current_direction'] = 'stop'
    snake['head'] = turtle.Turtle()
    snake['head'].shape(SNAKE_SHAPE)
    snake['head'].showturtle()
    snake['head'].pu()
    snake['head'].color('grey')
    snake["snakebody"] = []
    snake["coord"] = []
    create_score_board(state)
    create_food(state)

# Random background with decorations
def background(state):
    window = turtle.Screen()
    state['window'] = window
    n = randint(1, 3)
    if n == 1:
        state['window'].bgcolor('gray5')
    elif n == 2:
        state['window'].bgcolor('green')
        for i in range(20):
            terra = turtle.Turtle()
            terra.pu()
            terra.pencolor('brown4')
            terra.goto(randint(-MAX_X//2 + DEFAULT_SIZE//2, MAX_X//2 - DEFAULT_SIZE//2),
                       randint(-MAX_Y//2 + DEFAULT_SIZE//2, MAX_Y//2 - DEFAULT_SIZE//2))
            terra.shape('square')
            terra.turtlesize(DEFAULT_SIZE // 10)
            terra.fillcolor('brown4')
    elif n == 3:
        state['window'].bgcolor('cyan4')
        for i in range(30):
            bubble = turtle.Turtle()
            bubble.pu()
            bubble.pencolor('cyan')
            bubble.goto(randint(-MAX_X//2 + DEFAULT_SIZE//2, MAX_X//2 - DEFAULT_SIZE//2),
                        randint(-MAX_Y//2 + DEFAULT_SIZE//2, MAX_Y//2 - DEFAULT_SIZE//2))
            bubble.shape('circle')
            bubble.turtlesize(DEFAULT_SIZE // 15)
            bubble.fillcolor('cyan')

# Move snake head
def move_head(state):
    snake = state['snake']
    if snake["current_direction"] == "up":
        snake["head"].seth(90)
        snake["head"].fd(20)
    if snake["current_direction"] == "down":
        snake["head"].seth(270)
        snake["head"].fd(20)
    if snake["current_direction"] == "left":
        snake["head"].seth(180)
        snake["head"].fd(20)
    if snake["current_direction"] == "right":
        snake["head"].seth(0)
        snake["head"].fd(20)

# Move snake body segments
def move_body(state):
    snake = state["snake"]
    for i in range(len(snake["snakebody"])):
        snake['snakebody'][i].shape(SNAKE_SHAPE)
        snake['snakebody'][i].color('darkorange2' if i % 2 == 0 else 'darkorange3')
        snake["snakebody"][i].speed(SPEED)
        snake["snakebody"][i].pu()
        snake["snakebody"][i].goto(snake["coord"][i])
    if len(snake["coord"]) > len(snake["snakebody"]):
        snake["coord"].pop(-1)
    snake["coord"].insert(0, snake["head"].pos())

# Create food at random position
def create_food(state):
    food = turtle.Turtle()
    food.turtlesize(DEFAULT_SIZE / 25)
    food.pu()
    food.shape("circle")
    food.color("gold" if state["score"] >= state["high_score"] - 10 else "firebrick1")
    food.goto(randint(-MAX_X//2 + DEFAULT_SIZE//2, MAX_X//2 - DEFAULT_SIZE//2),
              randint(-MAX_Y//2 + DEFAULT_SIZE//2, MAX_Y//2 - DEFAULT_SIZE//2))
    state["food"] = food

# Check if snake eats food
def check_if_food_to_eat(state):
    food = state['food']
    snake = state["snake"]
    if snake["head"].distance(food) < 15:
        create_food(state)
        food.ht()
        snake["snakebody"].append(turtle.Turtle())
        state["score"] += 10
        if state["score"] >= state["high_score"]:
            state["high_score"] = state["score"]
            state["new_high_score"] = True
        else:
            state["new_high_score"] = False
    update_score_board(state)

# Check collisions with walls
def boundaries_collision(state):
    snake = state['snake']
    xsnake = snake["head"].xcor()
    ysnake = snake["head"].ycor()
    return xsnake < -MAX_X/2 + DEFAULT_SIZE/2 or xsnake > MAX_X/2 - DEFAULT_SIZE/2 or ysnake < -MAX_Y/2 + DEFAULT_SIZE/2 or ysnake > MAX_Y/2 - DEFAULT_SIZE/2

# Check collisions with body or walls
def check_collisions(state):
    snake = state["snake"]
    for segment in snake["snakebody"]:
        if snake["head"].distance(segment) < 19:
            return not boundaries_collision(state)
    return boundaries_collision(state)

def main():
    state = init_state()
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

# Entry point for script
if __name__ == "__main__":
    main()
