import turtle as turtle
from config import *
from random import randint

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