from config import *
from ui.food import create_food
import turtle as turtle

# Update score board display
def update_score_board(state):
    state['score_board'].clear()
    if state["score"] >= state["high_score"]:
        state["score_board"].color("gold")
    state['score_board'].write(
        "Score: {} High Score: {}".format(state['score'], state['high_score']), 
        align="center", font=("Comic Sans MS", 24, "normal")
    )


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
