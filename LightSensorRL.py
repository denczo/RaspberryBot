from tkinter import *
from PIL import Image
import time
from enum import Enum

class Directions(Enum):
    leftTurn = -1
    rightTurn = 0
    forward = 1

class Orientation(Enum):
    left = 0
    top = 1
    right = 2
    bottom = 3

currentOrientation = Orientation.bottom
#LIGHT SENSOR x1,x2,x3,y1,y2,y3
sensor = [2,3,4,15,15,15]

def borderCheck(value,max):
    if value > max-1:
        return 0
    elif value < 0:
        return max-1
    else:
        return value

def moveRight(sensor,max):
    for i in range(3):
        value = sensor[i]
        sensor[i] = borderCheck(value+1,max)

def moveLeft(sensor,max):
    for i in range(3):
        value = sensor[i]
        sensor[i] = borderCheck(value - 1, max)

def moveDown(sensor,max):
    for i in range(3):
        value = sensor[i+3]
        sensor[i+3] = borderCheck(value + 1, max)

def moveUp(sensor,max):
    for i in range(3):
        value = sensor[i+3]
        sensor[i+3] = borderCheck(value - 1, max)

def vertical(sensor, direction,max):
    global currentOrientation
    #compare y values
    #print(sensor)
    if sensor[4] == sensor[3] == sensor[5]:
        if direction == Directions.leftTurn:
            if sensor[0] < sensor[2]:
                sensor[3] -= 1
                sensor[5] += 1
            else:
                sensor[3] += 1
                sensor[5] -= 1
        elif direction == Directions.rightTurn:
            if sensor[0] < sensor[2]:
                sensor[3] += 1
                sensor[5] -= 1
            else:
                sensor[3] -= 1
                sensor[5] += 1

        sensor[0] = sensor[2] = sensor[1]
        for i in range(6):
            value = sensor[i]
            sensor[i] = borderCheck(value,max)

def horizontal(sensor,direction,max):
    global currentOrientation
    #compare x values
    #print(sensor)
    if sensor[1] == sensor[0] == sensor[2]:
        if direction == Directions.leftTurn:
            if sensor[3] < sensor[5]:
                sensor[0] -= 1
                sensor[2] += 1
            else:
                sensor[0] += 1
                sensor[2] -= 1
        elif direction == Directions.rightTurn:
            if sensor[3] < sensor[5]:
                sensor[0] += 1
                sensor[2] -= 1
            else:
                sensor[0] -= 1
                sensor[2] += 1

        sensor[3] = sensor[5] = sensor[4]
        for i in range(3):
            value = sensor[i]
            sensor[i] = borderCheck(value, max)
    #print(sensor[4],sensor[3],sensor[5])

def stupidLineFollower(sensor,height,values):

    if values[0] == 1 and values[1] == 0 and values[2] == 0:
        moveManagement(sensor,height,Directions.leftTurn)
        moveManagement(sensor, height, Directions.forward)
    elif values[0] == 0 and values[1] == 0 and values[2] == 1:
        moveManagement(sensor,height,Directions.rightTurn)
        moveManagement(sensor, height, Directions.forward)
    #elif values[1] == 1 or (values[0] == 0 and values[1] == 0 and values[2] == 0):
    else:
        moveManagement(sensor,height,Directions.forward)

#converts movement in proper orientation
def orientationCheck(orientation, direction):

    if direction == Directions.forward:
      return orientation

    elif orientation == Orientation.left:
        if direction == Directions.leftTurn:
            return Orientation.bottom
        elif direction == Directions.rightTurn:
            return Orientation.top

    elif orientation == Orientation.top:
        if direction == Directions.leftTurn:
            return Orientation.left
        elif direction == Directions.rightTurn:
            return Orientation.right

    elif orientation == Orientation.right:
        if direction == Directions.leftTurn:
            return Orientation.top
        elif direction == Directions.rightTurn:
            return Orientation.bottom

    elif orientation == Orientation.bottom:
        if direction == Directions.leftTurn:
            return Orientation.right
        elif direction == Directions.rightTurn:
            return Orientation.left

#does the proper movement for given orientation
def moveManagement(sensor,height,direction):
    global currentOrientation
    getOrientation = orientationCheck(currentOrientation,direction)
    #print(currentOrientation,direction)
    if direction == Directions.forward:

        if getOrientation == Orientation.left:
            moveLeft(sensor, height)
        elif getOrientation == Orientation.right:
            moveRight(sensor, height)
        elif getOrientation == Orientation.top:
            moveUp(sensor, height)
        elif getOrientation == Orientation.bottom:
            moveDown(sensor, height)

    else:

        if getOrientation == Orientation.left or getOrientation == Orientation.right:
            vertical(sensor,direction,height)
        elif getOrientation == Orientation.top or getOrientation == Orientation.bottom:
            horizontal(sensor,direction,height)

    currentOrientation = getOrientation


if __name__ == "__main__":
    master = Tk()
    w = Canvas(master, width=350, height=350)
    im = Image.open("TestBild2.png")
    width = im.size[0]
    height = im.size[1]
    bw_im = im.convert('L')
    size = 10
    gap = 2
    margin = 10
    values = [None]*(width*height)
    for x in range(width):
        for y in range(height):
            if (bw_im.getpixel((x, y)) < 255):
                values[width*x+y] = 1
            else:
                values[width*x+y] = 0

    counter = 0
    #test = [Directions.forward, Directions.rightTurn, Directions.forward, Directions.rightTurn, Directions.forward, Directions.rightTurn, Directions.forward, Directions.rightTurn]
    #test =[Directions.forward,Directions.leftTurn]
    while(1):
        w.delete("all")
        size = 10
        gap = 2
        margin = 10

        for x in range(width):
            x1 = x * (gap + size) + margin
            x2 = x1 + size

            for y in range(height):
                y1 = y * (gap + size) + margin
                y2 = y1 + size

                if (values[width*x+y] == 1):
                    w.create_rectangle(x1, y1, x2, y2, fill="black", outline="white")
                else:
                    w.create_rectangle(x1, y1, x2, y2, fill="white", outline="white")

        colors = [values[width*sensor[0]+sensor[3]],values[width*sensor[1]+sensor[4]],values[width*sensor[2]+sensor[5]]]
        #print(colors)
        stupidLineFollower(sensor,height,colors)
        #moveManagement(sensor, height, test[counter])
        #if counter < len(test)-1:
        #    counter += 1
        #else:
        #    counter = 0
        #print(counter)
        #print(counter)
        for x in range(3):
            x1 = sensor[x] * (gap + size) + margin
            x2 = x1 + size
            y1 = sensor[x+3] * (gap + size) + margin
            y2 = y1 + size
            w.create_rectangle(x1, y1, x2, y2, fill="", outline="red")

        w.pack()
        master.update_idletasks()
        master.update()
        time.sleep(0.5)