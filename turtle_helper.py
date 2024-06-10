import turtle

s = turtle.getscreen()

t = turtle.Turtle()

size = t.turtlesize()

increase = (2*num for num in size)

t.turtlesize(*increase)

t.pensize(5)
t.shapesize()
t.pencolor('blue')

def go_right():
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

def go_left():
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

def go_up():
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

def go_down():
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

def go_NE():
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

def go_NW():
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

def go_SW():
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

def go_SE():
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

def move(x, y, ismoving):
    if ismoving:
        if x == 1 and y == 0:
            go_right()
        elif x == 1 and y == 1:
            go_NE()
        elif x == 1 and y == -1:
            go_SE()
        elif x == 0 and y == 1:
            go_up()
        elif x == 0 and y == -1:
            go_down()
        elif x == -1 and y == 0:
            go_left()
        elif x == -1 and y == 1:
            go_NW()
        elif x == -1 and y == -1:
            go_SW()
        t.forward(150)         