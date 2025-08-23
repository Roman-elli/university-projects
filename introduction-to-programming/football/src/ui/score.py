import turtle as t

def create_score():
    score_board=t.Turtle()
    score_board.speed(0)
    score_board.color("Blue")
    score_board.penup()
    score_board.hideturtle()
    score_board.goto(0,260)
    score_board.write("Player A: 0\t\tPlayer B: 0 ", align="center", font=('Monaco',24,"normal"))
    return score_board