import turtle

def go_right(t):
    current = t.heading()
    if current == 0:
        pass
    elif current == 90:
        t.right(90)
    elif current == 180:
        t.right(180)
    elif current == 270:
        t.left(90)

def go_left(t):
    current = t.heading()
    if current == 180:
        pass
    elif current == 0:
        t.left(180)
    elif current == 90:
        t.left(90)
    elif current == 270:
        t.right(90)

def go_up(t):
    current = t.heading()
    if current == 90:
        pass
    elif current == 0:
        t.left(90)
    elif current == 180:
        t.right(90)
    elif current == 270:
        t.right(180)

def go_down(t):
    current = t.heading()
    if current == 270:
        pass
    elif current == 0:
        t.right(90)
    elif current == 90:
        t.left(180)
    elif current == 180:
        t.left(90)

def move(x, y, t, ismoving):
    if ismoving:
        if x == 1 and y == 0:
            go_right(t)
        elif x == 0 and y == 1:
            go_up(t)
        elif x == 0 and y == -1:
            go_down(t)
        elif x == -1 and y == 0:
            go_left(t)
        t.forward(0.5)         
