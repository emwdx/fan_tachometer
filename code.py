
import board
import analogio
import digitalio
import storage
import time



buttonA = digitalio.DigitalInOut(board.BUTTON_A)
buttonA.switch_to_input(pull=digitalio.Pull.DOWN)

buttonB = digitalio.DigitalInOut(board.BUTTON_B)
buttonB.switch_to_input(pull=digitalio.Pull.DOWN)

# Set up light sensor
light = analogio.AnalogIn(board.LIGHT)

SAMPLE_PERIOD = 0.001 # seconds
SAMPLE_SIZE = 100 # number of measurements to analyze at a time


# Set up lists to use for analysis
raw_values = [0]*SAMPLE_SIZE
light_values = [0]*SAMPLE_SIZE
saved_data =[]
num_transitions = 0

# This is a calibration step to figure out what threshold value to use.
# Press the button A value when the light sensor is dark
THRESHOLD = 0
print('calibrate dark value')
while(not buttonA.value):
    time.sleep(0.001)
dark_value = light.value
# Then press the button B value when the light sensor is bright
print('calibrate light value')
while(not buttonB.value):
    time.sleep(0.001)
bright_value = light.value
# Calculate the threshold as the average of these two values.
THRESHOLD = 0.5*(dark_value + bright_value)

elapsed_time = 0
start_time = time.monotonic()
stop_collecting = False

# This starts the data collection loop.
while not stop_collecting:
    current_time = time.monotonic()

    # Read the raw light value from the sensor
    raw_light = light.value
    # Add the light value to the list of raw values
    raw_values.append(raw_light)

    # Once enough data points have been collected, process the list of raw_values.

    if(len(raw_values)>= SAMPLE_SIZE):

        # Build a list  of thresholded values
        # When your code is working in Replit on your sample CSV, this is where you want to put your algorithm for processing.
        # Instead of going row by row through the CSV file, you want to go row by row through the list of raw values.
        for raw_light_value in raw_values:

            if(raw_light_value > THRESHOLD):
                light_value = 1
            else:
                light_value = 0
            light_values.append(light_value)

        # Go through the thresholded data and change the number of transitions whenever the values go from 0 to 1.
        for i in range(len(light_values)-1):
            if(light_values[i] == 0 and light_values[i+1] == 1):
                num_transitions += 1

        # Update the elapsed time based on how much time has gone by, and then print the data
        elapsed_time += current_time - start_time

        print("{0},{1}".format(elapsed_time,num_transitions))
        saved_data.append([elapsed_time,num_transitions])
        # Reset the lists of data for the next sample period.
        start_time = current_time
        raw_values = []
        light_values = []


    time.sleep(SAMPLE_PERIOD)
    # Stop showing data if buttonA is pressed
    if(buttonA.value == True):
        stop_collecting = True

led = digitalio.DigitalInOut(board.D13)
led.switch_to_output()

try:
    with open("light.csv", "a") as fp:
        print("opened")
        for row in saved_data:
            print(row)
            led.value = True
            fp.write("{0},{1}\n".format(row[0],row[1]))

        fp.close()
        led.value = False
except OSError as e:
    print(e)

