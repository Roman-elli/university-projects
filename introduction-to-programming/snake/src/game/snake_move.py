from config import *

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
