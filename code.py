# Fan Tachometer by Evan Weinberg (GitHub: emwdx, Twitter: @emwdx)
# This program uses the Circuit Playground Express on the back of a fan pointed at a light source to calculate rotation frequency.
# The units of frequency are in rotations/second. See the repository for more details.
#
#

import time
import board
from adafruit_circuitplayground import cp


#Define states for the light sensor
TRANSITION_OCCURRED = 2
BLOCKED = 1
UNBLOCKED = 0
currentState = UNBLOCKED

#Set global variables for keeping track of the system
transitions = 0
oldTime = 0
currentTime = 0
rotation_frequency = 0
average_rotation_frequency = 0
loopCount = 0
oldTransitions = 0
elapsedTime = 0

#Set the light sensor threshold between light and dark here.
SENSITIVITY = 20
#Set the number of fan blades
NUM_OF_BLADES = 3
#Set the number of frequency values to store in the array. More values results in smoother data, but slows down the responsiveness.
FREQ_SIZE = 100
freqs = [0]*FREQ_SIZE

#Define how frequently we want the frequency to be calculated (CALCULATE_INTERVAL) and how often to report data (REPORT_INTERVAL)
CALCULATE_INTERVAL = 100
REPORT_INTERVAL = 2000

#Define the style of the output printed to the console. This can be TABBED, PLOTTER_T_AND_F, PLOTTER_T_ONLY, PLOTTER_F_ONLY, or PLOTTER_ALL
PRINT_STYLE = "TABBED"
#PRINT_STYLE = "PLOTTER_T_AND_F"
#PRINT_STYLE = "PLOTTER_T_ONLY"
#PRINT_STYLE = "PLOTTER_F_ONLY"
#PRINT_STYLE = "PLOTTER_ALL"


#This is a state machine that tracks the light sensor detecting light and dark from the fan blades
def evaluateState(currentState):
    if(currentState == UNBLOCKED):
        if(cp.light < SENSITIVITY):
            currentState = BLOCKED

    elif(currentState == BLOCKED):
        if(cp.light>SENSITIVITY):
            currentState = TRANSITION_OCCURRED
    else:
        currentState = UNBLOCKED
    return currentState

#This function calculates the rotation speed of the fan.
def calculateRotationFrequency():
    global oldTime
    global oldTransitions
    global elapsedTime
    global average_rotation_frequency
    global freqs
    global changeInTime

    #See how much time has elapsed since the last calculation.
    currentTime = time.monotonic()
    changeInTransitions = transitions - oldTransitions
    changeInTime = currentTime - oldTime

    #This is necessary for the first loop to keep the elapsedTime variable from being the same as the clock of the CPE.
    if(changeInTime < 1.0):
        elapsedTime += changeInTime

    #This logic prevents errors that sometimes happen when there are no transitions.
    if(changeInTransitions > 0):
        if(currentTime > oldTime):
            #The fan blade constant ensures the frequency calculated is for the entire fan to rotate around.
            rotation_frequency = changeInTransitions / changeInTime / NUM_OF_BLADES
        else:
            rotation_frequency = average_rotation_frequency
    else:
        rotation_frequency = 0

    #This uses an array of frequency values to smooth out the frequency calculation.
    freqs.pop(0)
    freqs.append(changeInTransitions)
    average_rotation_frequency = (average_rotation_frequency*(FREQ_SIZE - 1)+ rotation_frequency)/FREQ_SIZE

    #Store values from this loop in the global variables.
    oldTransitions = transitions
    oldTime = currentTime

def printData():
    global loopCount
    global PRINT_STYLE

    loopCount = 0
    if(PRINT_STYLE == "TABBED"):
        print(str(elapsedTime) + "\t" + str(transitions) + "\t" + str(average_rotation_frequency))
    elif(PRINT_STYLE == "PLOTTER_T_AND_F"):
        print((transitions,average_rotation_frequency))
    elif(PRINT_STYLE == "PLOTTER_T_ONLY"):
        print((transitions,))
    elif(PRINT_STYLE == "PLOTTER_F_ONLY"):
        print((average_rotation_frequency,))
    else:
        print((cp.light,transitions,average_rotation_frequency))

while True:
    #Evaluate the state
    currentState = evaluateState(currentState)

    #If a transition has occurred, increase the transitions by 1.
    if(currentState == TRANSITION_OCCURRED):
        transitions += 1

    #The two intervals let us report and calculate the frequency at different rates.
    if(loopCount % CALCULATE_INTERVAL == 0):
        calculateRotationFrequency()
    if(loopCount == REPORT_INTERVAL):
        printData()
    else:
        loopCount += 1

    time.sleep(0.00005)
