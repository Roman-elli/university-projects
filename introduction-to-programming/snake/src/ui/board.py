import turtle as turtle
from game.game_state import update_score_board
from random import randint
from utils.file import load_high_score
from config import *
import time

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