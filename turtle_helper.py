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
    elif current == 45:
        t.right(45)
    elif current == 135:
        t.right(135)
    elif current == 225:
        t.left(135)
    elif current == 315:
        t.left(45)

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
    elif current == 45:
        t.left(135)
    elif current == 135:
        t.left(45)
    elif current == 225:
        t.right(45)
    elif current == 315:
        t.right(135)

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
    elif current == 45:
        t.left(45)
    elif current == 135:
        t.right(45)
    elif current == 225:
        t.right(135)
    elif current == 315:
        t.left(135)

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
    elif current == 45:
        t.right(135)
    elif current == 135:
        t.left(135)
    elif current == 225:
        t.left(45)
    elif current == 315:
        t.right(45)

def go_NE(t):
    current = t.heading()
    if current == 45:
        pass
    elif current == 0:
        t.left(45)
    elif current == 90:
        t.right(45)
    elif current == 180:
        t.right(135)
    elif current == 270:
        t.left(135)
    elif current == 135:
        t.right(90)
    elif current == 225:
        t.right(180)
    elif current == 315:
        t.left(90)

def go_NW(t):
    current = t.heading()
    if current == 135:
        pass
    elif current == 0:
        t.left(135)
    elif current == 90:
        t.left(45)
    elif current == 180:
        t.right(45)
    elif current == 270:
        t.right(135)
    elif current == 45:
        t.left(90)
    elif current == 225:
        t.right(90)
    elif current == 315:
        t.left(180)

def go_SW(t):
    current = t.heading()
    if current == 225:
        pass
    elif current == 0:
        t.right(135)
    elif current == 90:
        t.left(135)
    elif current == 180:
        t.left(45)
    elif current == 270:
        t.right(45)
    elif current == 45:
        t.right(180)
    elif current == 135:
        t.left(90)
    elif current == 315:
        t.right(90)

def go_SE(t):
    current = t.heading()
    if current == 315:
        pass
    elif current == 0:
        t.right(45)
    elif current == 90:
        t.right(135)
    elif current == 180:
        t.left(135)
    elif current == 270:
        t.left(45)
    elif current == 45:
        t.right(90)
    elif current == 135:
        t.left(180)
    elif current == 225:
        t.left(90)

def move(x, y, t, ismoving):
    if ismoving:
        if x == 1 and y == 0:
            go_right(t)
        elif x == 1 and y == 1:
            go_NE(t)
        elif x == 1 and y == -1:
            go_SE(t)
        elif x == 0 and y == 1:
            go_up(t)
        elif x == 0 and y == -1:
            go_down(t)
        elif x == -1 and y == 0:
            go_left(t)
        elif x == -1 and y == 1:
            go_NW(t)
        elif x == -1 and y == -1:
            go_SW(t)
        t.forward(1)         
