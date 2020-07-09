# fan_tachometer

Fan Tachometer by [Evan Weinberg](http://www.evanweinberg.com) (GitHub: [emwdx](https://github.com/emwdx), Twitter: [@emwdx](https://twitter.com/emwdx))

A program written in CircuitPython 5.3 for the Circuit Playground Express to measure the rotation speed of a fan.

This program uses the Circuit Playground Express on the back of a fan pointed at a light source to calculate rotation frequency in rotations per second. This uses the ambient light hitting the onboard light sensor. The sensor picks up on the light sensor changing as the fan blades block the light source. 

You should be able to clone the repository and then upload the entire directory to your Circuit Playground Express board. 

You can set some options to make this work for you beginning on line 10.

* SENSITIVITY - This is the light sensor threshold the program will use for light and dark. This should be in between the values for the light sensor reading with and without a fan blade in the way. Use the print setting "PLOTTER_ALL" to see what the sensor is reading.
* NUM_OF_BLADES - this divides the frequency of transitions by the number of fan blades to measure full rotations of the fan. Make this 1 if you want to see how many times the fan blades are going past per second.
* FREQ_SIZE - The program uses an array of frequency values that are averaged together to get the average frequency for each calculation interval. This variable sets how big you want this array to be. Bigger values smooth out the frequency data more.
* CALCULATE_INTERVAL and REPORT_INTERVAL - the program calculates at a different rate than it is printed to the console. This keeps the console from becoming overloaded while also maintaining a high frequency for updating the value. These are both measured in the number of loops that should happen before calculating or reporting.
* PRINT_STYLE - You can set this to print in a few different ways. FRIENDLY gives all system measurements with units. TABBED will make it easy to copy and paste into Desmos or another CSV-friendly tool. The others use the plotter function in [Mu-Editor](https://codewith.mu) to display different sets of values and print them to the console. The values are "FRIENDLY","TABBED", "PLOTTER_T_AND_F", "PLOTTER_T_ONLY", "PLOTTER_F_ONLY", or "PLOTTER_ALL". Uncomment the one you want to use.

I wrote this also as an example of using a state machine and modular code for my Advanced Automation class next year. I use some states to track the changes in the light sensor in the function called evaluateState. I also make separate functions for calculating the average frequency and printing data. Go to the while loop at the bottom to see how this works.


