import RPi.GPIO as GPIO
import time
import pigpio
import random

servoPins = [9,10]
sensorPins = [17,27,22]
pi = pigpio.pi()


#sensor has 3 inputs
sensorStates = ['000','001','010','011','100','101','110','111']
Qsa = [0.0]*len(sensorStates)*3 #3 = amount of possible movements

learningRate = 0.4
discountRate = 0.7
#oldSensorStateIndex = 0
prevStateIndex = 0
maxActionIndex = 0
tau = 0.2
delta = 0

# 1000 spin fast anticlockwise
# 1400 spin slow anticlockwise
# 1500 stop
# 1600 spin slow clockwise
# 2000 spin fast clockwise

def checkReward(sensorValues):
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
    for i in range(3):
        currentQsa = Qsa[countStates*i+stateIndex]
        print(Qsa)
        if currentQsa > oldQsa:
            oldQsa = currentQsa
            oldMaxAction = i
            found = True

    epsilon = 0
    if tau > 0.2:
        epsilon = random.randint(0,100)
    else:
        epsilon = 100

    #epsilon greedy
    #if not(found) or epsilon >= 0.6:
    if not(found):
        return random.randint(0,2)
    else:
        return oldMaxAction

def getStateIndex(sensorValues,sensorStates):
    binaryValue = str(sensorValues[0]) + str(sensorValues[1]) + str(sensorValues[2])
    index = 0
    for i in range(len(sensorStates)):
        if sensorStates[i] == binaryValue:
            index = i

    return index

def updateQs(sensorValues, sensorStates):
    global  prevStateIndex, maxActionIndex
    #actionIndex = getActionIndex(direction)
    stateIndex = getStateIndex(sensorValues,sensorStates)
    prevQsa = Qsa[len(sensorStates) * maxActionIndex + prevStateIndex]
    reward = checkReward(sensorValues)

    oldActionIndex = maxActionIndex
    maxActionIndex = getMaxAction(Qsa,stateIndex,len(sensorStates))
    #print("prev QSA (", prevStateIndex, oldActionIndex, ") maxAction",maxActionIndex)

    #print(len(sensorStates)*maxActionIndex+stateIndex)
    currentQsa = Qsa[len(sensorStates) * maxActionIndex + stateIndex]
    Qsa[len(sensorStates) * oldActionIndex + prevStateIndex] = (1 - learningRate) * prevQsa + learningRate*(reward+discountRate*currentQsa)
    prevStateIndex = stateIndex
    updateMovement(maxActionIndex)

def updateMovement(maxActionIndex):
    if maxActionIndex == 0:
        moveLeft()
    elif maxActionIndex == 1:
        moveForward()
    elif maxActionIndex == 2:
        moveRight()

def moveLeft():
    pi.set_servo_pulsewidth(servoPins[0],1450)
    pi.set_servo_pulsewidth(servoPins[1], 0)
    time.sleep(0.1)

def moveRight():
    pi.set_servo_pulsewidth(servoPins[0], 0)
    pi.set_servo_pulsewidth(servoPins[1],1520)
    time.sleep(0.1)

def moveForward():
    pi.set_servo_pulsewidth(servoPins[0], 1450)
    pi.set_servo_pulsewidth(servoPins[1], 1520)
    time.sleep(0.1)

def read():
    for i in range(len(sensorPins)):
        GPIO.setup(sensorPins[i], GPIO.OUT)
        GPIO.output(sensorPins[i], True) #Drive the output high, charging the capacitor
        time.sleep(0.01) #wait for the cap to charge. Equations available on wikipe$
    count = [0,0,0] # set the counter to 0
    for i in range(len(sensorPins)):
        GPIO.setup(sensorPins[i], GPIO.IN) # set pin to input
        while GPIO.input(sensorPins[i]) == True:
            count[i] = count[i] + 1
    return count

def editData(data):
    editedData = [0,0,0]
    for i in range(len(data)):
        if data[i] < 15:
            editedData[i] = 0
        else:
            editedData[i] = 1
    return editedData

if __name__ == "__main__":

    GPIO.setmode(GPIO.BCM)

    try:
        while True:
            #print(read())
            values = [0,0,0]
            values = editData(read())
            #print(values)
            updateQs(values,sensorStates)

            """
            if values[0] == 1 and (values[1] == 0 or values[1] == 1) and values[2] == 0:
                moveLeft()
            elif values[0] == 0 and (values[1] == 0 or values[1] == 1) and values[2] == 1:
                moveRight()
            else:
                moveForward()
            #time.sleep(1)
            """

    except KeyboardInterrupt:
        pi.set_servo_pulsewidth(servoPins[0], 0)
        pi.set_servo_pulsewidth(servoPins[1], 0)
        pi.stop()
        GPIO.cleanup()
