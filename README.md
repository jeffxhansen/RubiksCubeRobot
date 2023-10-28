# Jeff Hansen Rubik's Cube Robot

## Files Outline

* **Cube.py** this is the primary brain and thinking portion of the robot. This stores all of the color values of the cube as numbers in a 48 length array. This class handles all of the computation and uses the ZZ method and the associated algorithms to find a solution to the Rubik's Cube.

* **Robot.py** This is the Motor / Camera / Rubik's Cube interface that handles all of the motor movements and translates the Rubik's Cube solution from `Cube.py` into actual motor movements

* **cameraSensor.py** This handles all of the computer vision and acts as a class inside of the Robot class. It uses OpenCV to take pictures, convert to numpy arrays, and perform the calculations for color recognition. I treat colors as 3 dimensional vectors, and I use cosine similarity for color classification

* **maestro/maestro.py** This is a Github repo that I imported that is incorporated with the Pololu Maestro Servo controller. This translates the serial output from the raspberry pi to signals that the servos understand.

* **main.py** the `run()` function actually runs the robot in this file. This file is large and generally just filled with lots of unit tests for different portions of the robot.

* **alogorithms/** These files house all of the 400+ algoriths used in the ZZ method to solve the last layer of the Rubik's Cube. I used the `imageProcessor.py` class to speed up the process by downloading images from the internet and converting to numeric strings, so the Rubik's cube robot can genearte a hash-map lookup table to find which algorithm will solve the last layer

* **quick_scripts/** Lots of other files used to do unit tests, test out certain aspects of the code, and supllementary files that helped me formulate how to code this Rubik's Cube Robot