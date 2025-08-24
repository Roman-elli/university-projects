import turtle as t
from config import *
import random

def reset_ball_position(ball):
    ball.setpos(BALL_START_POS)
    x = random.randrange(360)
    ball.setheading(x)

def draw_ball():
    ball = t.Turtle()
    ball.penup()
    ball.shapesize(1)
    ball.shape("circle")
    ball.color("black")
    reset_ball_position(ball)
    ball.speed(MOVE_PIXELS*1.2)
    dic_bola = {'ball': ball,'x_coordinate': ball.xcor(), 'y_coordinate': ball.ycor(), 'previous_position': None}

    return dic_bola