from tkinter import *
from PIL import Image
import time
import copy
from enum import Enum

im = Image.open("TestBild.png")
width = im.size[0]
height = im.size[1]

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


def moveRight(sensor,max,direction):
    vertical(sensor,direction,max)
    for i in range(3):
        value = sensor[i]
        sensor[i] = borderCheck(value+1,max)

def moveLeft(sensor,max,direction):
    vertical(sensor, direction, max)
    for i in range(3):
        value = sensor[i]
        sensor[i] = borderCheck(value - 1, max)

def moveDown(sensor,max,direction):
    horizontal(sensor,direction,max)
    for i in range(3):
        value = sensor[i+3]
        sensor[i+3] = borderCheck(value + 1, max)

def moveUp(sensor,max,direction):
    horizontal(sensor, direction, max)
    for i in range(3):
        value = sensor[i+3]
        sensor[i+3] = borderCheck(value - 1, max)

def vertical(sensor, direction,max):
    global currentOrientation
    #compare y values
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

        sensor[0] = sensor[2] = sensor[1]
        for i in range(3):
            value = sensor[i]
            sensor[i] = borderCheck(value, max)
    #print(sensor[4],sensor[3],sensor[5])
"""
def orientation(sensor,height,orientation):

    if orientation == Orientation.left:
        #vertical(sensor,Directions.leftTurn,height)
        moveRight(sensor,height)
    elif orientation == Orientation.right:
        #vertical(sensor, Directions.rightTurn, height)
        moveLeft(sensor,height)
    elif orientation == Orientation.top:
        #horizontal(sensor,Directions.forward,height)
        moveUp(sensor,height)
    elif orientation == Orientation.bottom:
        #horizontal(sensor,Directions.forward,height)
        moveDown(sensor,height)
"""
def stupidLineFollower(sensor,height,values):

    #print(sensor,height,values)
    if ((values[1] == 0 and values[2] == 1) or (values[1] == 1 and values[2] == 1)) and (Orientation.top or Orientation.bottom):
        orientation(sensor,height,Orientation.left)
    elif ((values[0] == 1 and values[1] == 0) or (values[0] == 1 and values[1] == 1))and (Orientation.top or Orientation.bottom):
        orientation(sensor, height, Orientation.right)
    else:
        print("NOPE")
        pass
        #orientation(sensor, height, Orientation.bottom)

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
    print(currentOrientation,direction)
    if getOrientation == Orientation.left:
        moveLeft(sensor, height,direction)
    elif getOrientation == Orientation.right:
        moveRight(sensor, height,direction)
    elif getOrientation == Orientation.top:
        moveUp(sensor, height,direction)
    elif getOrientation == Orientation.bottom:
        moveDown(sensor, height,direction)

    currentOrientation = getOrientation


if __name__ == "__main__":
    master = Tk()
    w = Canvas(master, width=350, height=350)
    #im = Image.open("TestBild.png")
    #width = im.size[0]
    #height = im.size[1]
    bw_im = im.convert('L')
    size = 10
    gap = 2
    margin = 10
    values = [None]*(width*height)
    for x in range(width):
        for y in range(height):
            if (bw_im.getpixel((x, y)) < 128):
                values[width*x+y] = 1
            else:
                values[width*x+y] = 0

    counter = 0
    test = [Directions.rightTurn]
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


        moveManagement(sensor, height, test[counter])
        if counter < len(test)-1:
            counter += 1

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
        time.sleep(1)