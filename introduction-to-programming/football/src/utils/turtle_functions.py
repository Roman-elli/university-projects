import turtle as t
from config import *

def save_movement(dic):
    dic['x_coordinate'] = dic['player'].xcor()
    dic['y_coordinate'] = dic['player'].ycor()

def turtle_go_to(x,y, draw):
    draw.penup()
    draw.goto(x,y)
    draw.pendown()
