from tkinter import *
from PIL import Image
import time
from enum import Enum
import random
import numpy
import math

class Directions(Enum):
    leftTurn = -1
    rightTurn = 0
    forward = 1

class Orientation(Enum):
    left = 0
    top = 1
    right = 2
    bottom = 3

#sensor has 3 inputs
sensorStates = ['000','001','010','011','100','101','110','111']
Qsa = [0.0]*len(sensorStates)*3 #3 = amount of possible movements
#startOrientation
currentOrientation = Orientation.bottom
#LIGHT SENSOR x1,x2,x3,y1,y2,y3
sensor = [2,3,4,15,15,15]
#sensor = [1,2,3,15,15,15]

learningRate = 0.4
discountRate = 0.7
#oldSensorStateIndex = 0
prevStateIndex = 0
maxActionIndex = 0
tau = 0.2
delta = 0


def softmax(Qsa, stateIndex, countStates, stateQvalue, tau):

    tau = round(tau,6)
    #print(tau)

    numerator = math.exp(stateQvalue/tau)
    denumerator = 0

    for i in range(int(len(Qsa)/countStates)):
        denumerator += math.exp((Qsa[countStates*i+stateIndex])/tau)

    return numerator/denumerator

def getActionIndex(direction):

    if direction == Directions.leftTurn:
        return 0
    elif direction == Directions.forward:
        return 1
    elif direction == Directions.rightTurn:
        return 2

def getStateIndex(sensorValues,sensorStates):
    binaryValue = str(sensorValues[0]) + str(sensorValues[1]) + str(sensorValues[2])
    index = 0
    for i in range(len(sensorStates)):
        if sensorStates[i] == binaryValue:
            index = i


    return index

def checkReward(sensorValues, sensorStates):
    binaryValue = str(sensorValues[0]) + str(sensorValues[1]) + str(sensorValues[2])
    if binaryValue == '000':
        return -1
    elif (binaryValue == '010'):
        return 10
    else:
        return 0

def getMaxAction(Qsa, stateIndex, countStates):
    found = False
    oldQsa = 0
    oldMaxAction = 0
    #for i in range(3):
        #currentQsa = Qsa[countStates*i+stateIndex]
        #print(Qsa)
        #if currentQsa > oldQsa:
            #oldMaxAction = i
            #found = True

    turnLeft = softmax(Qsa, stateIndex, countStates, Qsa[countStates*0+stateIndex],tau)
    forward = softmax(Qsa, stateIndex, countStates, Qsa[countStates*1+stateIndex],tau)
    turnRight = softmax(Qsa, stateIndex, countStates, Qsa[countStates*2+stateIndex],tau)
    #print(turnLeft,forward,turnRight)
    #print(Qsa)




    if turnLeft-delta > forward and turnLeft-delta > turnRight:
        return 0
    elif turnRight-delta > forward and turnRight-delta > turnLeft:
        return 2
    elif forward-delta > turnRight and forward-delta > turnLeft:
        return 1
    else:

        print("RANDOM",tau)
        return random.randint(0,2)

    #epsilon greedy
    #epsilon = random.randint(0,6)/10

    #if not(found) or epsilon >= 0.6:
    #if not(found):
        #return random.randint(0,2)
    #else:
        #return oldMaxAction


def updateQs(sensor, sensorValues, sensorStates):
    global  prevStateIndex, maxActionIndex
    #actionIndex = getActionIndex(direction)
    stateIndex = getStateIndex(sensorValues,sensorStates)
    prevQsa = Qsa[len(sensorStates) * maxActionIndex + prevStateIndex]
    reward = checkReward(sensorValues,sensorStates)

    oldActionIndex = maxActionIndex
    maxActionIndex = getMaxAction(Qsa,stateIndex,len(sensorStates))
    #print("prev QSA (", prevStateIndex, oldActionIndex, ") maxAction",maxActionIndex)

    #print(len(sensorStates)*maxActionIndex+stateIndex)
    currentQsa = Qsa[len(sensorStates) * maxActionIndex + stateIndex]
    Qsa[len(sensorStates) * oldActionIndex + prevStateIndex] = (1 - learningRate) * prevQsa + learningRate*(reward+discountRate*currentQsa)
    prevStateIndex = stateIndex
    updateMovement(maxActionIndex,sensor,height)

def updateMovement(maxActionIndex, sensor, height):
    direction = 0
    if maxActionIndex == 0:
        direction = Directions.leftTurn
        moveManagement(sensor, height, direction)
        moveManagement(sensor, height, Directions.forward)
    elif maxActionIndex == 1:
        direction = Directions.forward
        moveManagement(sensor, height, direction)
    elif maxActionIndex == 2:
        direction = Directions.rightTurn
        moveManagement(sensor, height, direction)
        moveManagement(sensor, height, Directions.forward)


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

    #print(values)
    if values[0] == 1 and (values[1] == 0 or values[1] == 1) and values[2] == 0:
        moveManagement(sensor,height,Directions.leftTurn)
        moveManagement(sensor, height, Directions.forward)
    elif values[0] == 0 and (values[1] == 0 or values[1] == 1) and values[2] == 1:
        moveManagement(sensor,height,Directions.rightTurn)
        moveManagement(sensor, height, Directions.forward)
    #elif values[0] == 1 and values[1] == 1 and values[2] == 1:
        #choice = random.choice([Directions.rightTurn,Directions.leftTurn])
        #moveManagement(sensor, height, choice)
        #moveManagement(sensor, height, Directions.forward)
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
            return Orientation.right
        elif direction == Directions.rightTurn:
            return Orientation.left

    elif orientation == Orientation.right:
        if direction == Directions.leftTurn:
            return Orientation.top
        elif direction == Directions.rightTurn:
            return Orientation.bottom

    elif orientation == Orientation.bottom:
        if direction == Directions.leftTurn:
            return Orientation.left
        elif direction == Directions.rightTurn:
            return Orientation.right

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
            moveDown(sensor, height)
        elif getOrientation == Orientation.bottom:
            moveUp(sensor, height)

    else:

        if getOrientation == Orientation.left or getOrientation == Orientation.right:
            vertical(sensor,direction,height)
        elif getOrientation == Orientation.top or getOrientation == Orientation.bottom:
            horizontal(sensor,direction,height)

    currentOrientation = getOrientation


if __name__ == "__main__":
    master = Tk()
    w = Canvas(master, width=350, height=350)
    im = Image.open("TestBild4.png")
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


    while(1):

        if tau > 5:
            tau -= 1
        elif tau > 0.2:
            tau -= 0.1

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
        updateQs(sensor,colors,sensorStates)
        #stupidLineFollower(sensor,height,colors)

        for x in range(3):
            x1 = sensor[x] * (gap + size) + margin
            x2 = x1 + size
            y1 = sensor[x+3] * (gap + size) + margin
            y2 = y1 + size
            w.create_rectangle(x1, y1, x2, y2, fill="", outline="red")

        w.pack()
        master.update_idletasks()
        master.update()
        time.sleep(0.01)