import random
from tkinter import *
import keyboard


class square():
    def __init__(self, r, l):
        self.rectangle = r
        self.location = l


window = Tk()
window.geometry("500x600")
window.title("Snake")
canvas = Canvas(width=500, height=500)
rectangles = []
for i in range(25):
    for j in range(25):
        rectangles.append(
            canvas.create_rectangle(0 + (20 * i), 0 + (20 * j), 20 + (20 * i), 20 + (20 * j), fill='black'))
apples = []
snake = []
speed = Scale()
direction = "RIGHT"
updated = False
gamespeed = 300
loop = ''
snake.append(square(rectangles[312], 312))
canvas.itemconfig(snake[0].rectangle, fill='green')

for r in random.choices(rectangles, k=5):
    apples.append(rectangles.index(r))
    canvas.itemconfig(r, fill='red')


def update():
    global updated, snake, rectangles, loop
    locs = []
    for i in range(1, len(snake)):
        locs.append(snake[i].location)
    if snake[0].location in apples:
        apples.remove(snake[0].location)
        newapple = random.choice(range(0, 624))
        while newapple in apples or newapple in locs:
            newapple = random.choice(range(0, 624))
        apples.append(newapple)
        canvas.itemconfig(rectangles[newapple], fill='red')
        snake.append(square(snake[len(snake) - 1].rectangle, snake[len(snake) - 1].location))
    elif (snake[0].location % 25 == 0 and direction == "UP") or (
            (snake[0].location + 1) % 25 == 0 and direction == "DOWN"):
        for r in rectangles:
            canvas.itemconfig(r, fill='red')
        return
    try:
        oldEnd = snake[len(snake) - 1].rectangle
        for j in reversed(range(1, len(snake))):
            snake[j].rectangle = snake[j - 1].rectangle
            snake[j].location = snake[j - 1].location
        if direction == "UP":
            snake[0].location -= 1
            if snake[0].location in locs:
                for r in rectangles:
                    canvas.itemconfig(r, fill='red')
                return
            snake[0].rectangle = rectangles[snake[0].location]
            canvas.itemconfig(snake[0].rectangle, fill='green')
        elif direction == "LEFT":
            snake[0].location -= 25
            if snake[0].location < 0 or snake[0].location in locs:
                for r in rectangles:
                    canvas.itemconfig(r, fill='red')
                return
            snake[0].rectangle = rectangles[snake[0].location]
            canvas.itemconfig(snake[0].rectangle, fill='green')
        elif direction == "DOWN":
            snake[0].location += 1
            if snake[0].location in locs:
                for r in rectangles:
                    canvas.itemconfig(r, fill='red')
                return
            snake[0].rectangle = rectangles[snake[0].location]
            canvas.itemconfig(snake[0].rectangle, fill='green')
        elif direction == "RIGHT":
            snake[0].location += 25
            if snake[0].location > 624 or snake[0].location in locs:
                for r in rectangles:
                    canvas.itemconfig(r, fill='red')
                return
            snake[0].rectangle = rectangles[snake[0].location]
            canvas.itemconfig(snake[0].rectangle, fill='green')
    except IndexError:
        pass
    canvas.itemconfig(oldEnd, fill='black')
    updated = False
    canvas.pack()
    loop = window.after(gamespeed, update)


def keyboardListener():
    global direction, updated
    if not updated:
        if keyboard.is_pressed('w') and direction != "UP" and direction != "DOWN":
            direction = "UP"
            updated = True
        elif keyboard.is_pressed('a') and direction != "LEFT" and direction != "RIGHT":
            direction = "LEFT"
            updated = True
        elif keyboard.is_pressed('s') and direction != "UP" and direction != "DOWN":
            direction = "DOWN"
            updated = True
        elif keyboard.is_pressed('d') and direction != "LEFT" and direction != "RIGHT":
            direction = "RIGHT"
            updated = True
    window.after(55, keyboardListener)


def sliderchange(s):
    global gamespeed
    gamespeed = speed.get() * 100


def resetboard():
    global rectangles, snake, direction, apples
    snake = []
    apples = []
    for i in range(625):
        canvas.itemconfig(rectangles[i], fill='black')
    for r in random.choices(rectangles, k=5):
        apples.append(rectangles.index(r))
        canvas.itemconfig(r, fill='red')
    snake.append(square(rectangles[312], 312))
    canvas.itemconfig(snake[0].rectangle, fill='green')
    direction = "RIGHT"
    window.after_cancel(loop)
    update()


update()
keyboardListener()

restart = Button(text='Restart', command=resetboard)
restart.place(x=200, y=505, width=100, height=50)
speedlabal = Label(text="Speed:")
speedlabal.place(x=30, y=573)
speed = Scale(from_=1, to=10, length=350, orient=HORIZONTAL, command=sliderchange)
speed.set(3)
speed.place(x=80, y=555)

window.mainloop()
