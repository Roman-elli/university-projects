import time
from random import randint
import functools
import turtle

MAX_X = 600
MAX_Y = 640
DEFAULT_SIZE = 20
SNAKE_SHAPE = 'square'
HIGH_SCORES_FILE_PATH = 'high_scores.txt'
SPEED = 0.12


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


def write_high_score_to_file(state):
    with open(HIGH_SCORES_FILE_PATH, "a+") as statehs:
        print("NEW HIGHSCORE!!!")
        statehs.write("\n")
        statehs.write(str(state["high_score"]))
        statehs.close()


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


def create_lose_board(state):
    lose = turtle.Turtle()
    lose.speed(0)
    lose.shape("square")
    lose.color("chocolate3")
    lose.penup()
    lose.hideturtle()
    lose.goto(0, 0)
    if state["new_high_score"]:
        lose.write("NEW HIGHSCORE!! CONGRATULAIONS!!".format(), align="center", font=("Comic Sans MS", 15, "normal"))
    else:
        lose.write("YOU LOSE ! ! !".format(), align="center", font=("Comic Sans MS", 15, "normal"))

    time.sleep(2)


def update_score_board(state):
    state['score_board'].clear()
    if state["score"] >= state["high_score"]:
        state["score_board"].color("gold")
    state['score_board'].write("Score: {} High Score: {}".format(state['score'], state['high_score']), align="center", font=("Comic Sans MS", 24, "normal"))


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


def init_state():
    state = {'score_board': None, 'new_high_score': False, 'high_score': 0, 'score': 0, 'food': None, 'window': None, "player": ""}

    snake = {
        'head': None,
        'current_direction': None
    }
    state['snake'] = snake
    return state


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
            terracorx = randint(((-MAX_X // 2) + DEFAULT_SIZE // 2), ((MAX_X // 2) - DEFAULT_SIZE // 2))
            terracory = randint(((-MAX_Y // 2) + DEFAULT_SIZE // 2), ((MAX_Y // 2) - DEFAULT_SIZE // 2))
            terra.goto(terracorx, terracory)
            terra.shape('square')
            terra.turtlesize(DEFAULT_SIZE // 10)
            terra.fillcolor('brown4')
    elif n == 3:
        state['window'].bgcolor('cyan4')
        for i in range(30):
            bubble = turtle.Turtle()
            bubble.pu()
            bubble.pencolor('cyan')
            bubblecorx = randint(((-MAX_X // 2) + DEFAULT_SIZE // 2), ((MAX_X // 2) - DEFAULT_SIZE // 2))
            bubblecory = randint(((-MAX_Y // 2) + DEFAULT_SIZE // 2), ((MAX_Y // 2) - DEFAULT_SIZE // 2))
            bubble.goto(bubblecorx, bubblecory)
            bubble.shape('circle')
            bubble.turtlesize(DEFAULT_SIZE // 15)
            bubble.fillcolor('cyan')


def move(state):
    snake = state['snake']
    if (snake["current_direction"]) == "up":
        snake["head"].seth(90)
        snake["head"].fd(20)
    if (snake["current_direction"]) == "down":
        snake["head"].seth(270)
        snake["head"].fd(20)
    if (snake["current_direction"]) == "left":
        snake["head"].seth(180)
        snake["head"].fd(20)
    if (snake["current_direction"]) == "right":
        snake["head"].seth(0)
        snake["head"].fd(20)


def move2(state):
    snake = state["snake"]
    for i in range(len(snake["snakebody"])):
        snake['snakebody'][i].shape(SNAKE_SHAPE)
        if i % 2 == 0:
            snake['snakebody'][i].color('darkorange2')
        else:
            snake['snakebody'][i].color('darkorange3')
        snake["snakebody"][i].speed(SPEED)
        snake["snakebody"][i].pu()
        snake["snakebody"][i].goto(snake["coord"][i])

    if len(snake["coord"]) > len(snake["snakebody"]):
        snake["coord"].pop(-1)

    snake["coord"].insert(0, snake["head"].pos())

def create_food(state):
    food = state["food"]
    food = turtle.Turtle()
    food.turtlesize(DEFAULT_SIZE / 25)
    food.pu()
    food.shape("circle")
    if state["score"] >= state["high_score"] - 10:
        food.color("gold")
    else:
        food.color("firebrick1")
    foodcorx = randint(((-MAX_X // 2) + DEFAULT_SIZE // 2), ((MAX_X // 2) - DEFAULT_SIZE // 2))
    foodcory = randint(((-MAX_Y // 2) + DEFAULT_SIZE // 2), ((MAX_Y // 2) - DEFAULT_SIZE // 2))
    food.goto(foodcorx, foodcory)
    state["food"] = food

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
            if not (state["new_high_score"]):
                state["new_high_score"] = True
        else:
            state["new_high_score"] = False
    update_score_board(state)

def boundaries_collision(state):
    snake = state['snake']
    xsnake = snake["head"].xcor()
    ysnake = snake["head"].ycor()
    if (xsnake < ((-MAX_X / 2) + DEFAULT_SIZE / 2) or xsnake > ((MAX_X / 2) - DEFAULT_SIZE / 2) or ysnake < (
            (-MAX_Y / 2) + DEFAULT_SIZE / 2) or ysnake > ((MAX_Y / 2) - DEFAULT_SIZE / 2)):
        return True
    return False


def check_collisions(state):
    snake = state["snake"]
    for i in range(len(snake["snakebody"])):
        if snake["head"].distance(snake["snakebody"][i]) < 19:
            return not boundaries_collision(state)
    return boundaries_collision(state)


def main():
    state = init_state()
    setup(state)
    while not check_collisions(state):
        state['window'].update()
        check_if_food_to_eat(state)
        move(state)
        move2(state)
        time.sleep(SPEED)
    print("YOU LOSE!")
    create_lose_board(state)
    if state['new_high_score']:
        write_high_score_to_file(state)

main()