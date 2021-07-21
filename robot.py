
from Maestro.constants import *
import time

# sets the robot to the default open position
def defaultOpen():
    print("Setting robot to default open position")

    # for simultaneous motor movoment, multiple motors take turns incrementing small amounts
    # step determines the number of turns each motor takes (i.e number of iterations of the loop)
    step = 5

    # increment values for each motor, used in the loop
    increment1 = int((S1_END - S1_INIT)/step)
    increment2 = int((S2_END - S2_INIT)/step)
    increment3 = int((S3_END - S3_INIT)/step)
    increment4 = int((S4_END - S4_INIT)/step)

    # target position at the end of each iteration
    position1 = int(S1_INIT)
    position2 = int(S2_INIT)
    position3 = int(S3_INIT)
    position4 = int(S4_INIT)

    # set each motor to a slow acceleration
    servo.setAccel(M1, ACCEL_SLOW)
    servo.setAccel(S1, ACCEL_SLOW)
    servo.setAccel(M2, ACCEL_SLOW)
    servo.setAccel(S2, ACCEL_SLOW)
    servo.setAccel(M3, ACCEL_SLOW)
    servo.setAccel(S3, ACCEL_SLOW)
    servo.setAccel(M4, ACCEL_SLOW)
    servo.setAccel(S4, ACCEL_SLOW)

    # move all sliders out symultanesously
    for i in range(step):
        if i < step-1:
            servo.setTarget(S1, position1)
            servo.setTarget(S2, position2)
            servo.setTarget(S3, position3)
            servo.setTarget(S4, position4)

            position1 += increment1
            position2 += increment2
            position3 += increment3
            position4 += increment4
        else: # if i == step-1, or the last iteration
            servo.setTarget(S1, S1_END)
            servo.setTarget(S2, S2_END)
            servo.setTarget(S3, S3_END)
            servo.setTarget(S4, S4_END)

    time.sleep(SLEEP)

    # move gripppers to default positions
    servo.setTarget(M1, M1_INIT)
    servo.setTarget(M2, M2_INIT)
    servo.setTarget(M3, M3_INIT)
    servo.setTarget(M4, M4_INIT)

# sets the robot to the default closed position
def defaultClose():
    print("Setting robot to default closed position")

    time.sleep(SLEEP)

    # for simultaneous motor movoment, multiple motors take turns incrementing small amounts
    # step determines the number of turns each motor takes (i.e number of iterations of the loop)
    step = 5

    # increment values for each motor, used in the loop
    increment1 = int((S1_END - S1_INIT)/step)
    increment2 = int((S2_END - S2_INIT)/step)
    increment3 = int((S3_END - S3_INIT)/step)
    increment4 = int((S4_END - S4_INIT)/step)

    # target position at the end of each iteration
    position1 = int(S1_END)
    position2 = int(S2_END)
    position3 = int(S3_END)
    position4 = int(S4_END)

    servo.setTarget(M1, M1_INIT)
    servo.setTarget(M2, M2_INIT)
    servo.setTarget(M3, M3_INIT)
    servo.setTarget(M4, M4_INIT)

    for i in range(step):

        servo.setTarget(S2, position2)
        servo.setTarget(S4, position4)

        position2 -= increment2
        position4 -= increment4

        if i == step-1:
            servo.setTarget(S2, S2_INIT)
            servo.setTarget(S4, S4_INIT)

        time.sleep(SHORT)
    
    time.sleep(MEDIUM)

    for i in range(step):

        servo.setTarget(S1, position1)
        servo.setTarget(S3, position3)

        position1 -= increment1
        position3 -= increment3

        if i == step-1:
            servo.setTarget(S1, S1_INIT)
            servo.setTarget(S3, S3_INIT)
        
        time.sleep(SHORT)

def acceptCube():
    defaultOpen()
    time.sleep(SLEEP)
    defaultClose()
    time.sleep(SHORT)


def inDefaultPosition(motor):
    if motor == M1:
        if servo.getPosition(motor) == M1_INIT:
            return True
    elif motor == M2:
        if servo.getPosition(motor) == M2_INIT:
            return True
    elif motor == M3:
        if servo.getPosition(motor) == M3_INIT:
            return True
    elif motor == M4:
        if servo.getPosition(motor) == M4_INIT:
            return True
    elif motor == S1:
        if servo.getPosition(motor) == S1_INIT:
            return True
    elif motor == S2:
        if servo.getPosition(motor) == S2_INIT:
            return True
    elif motor == S3:
        if servo.getPosition(motor) == S3_INIT:
            return True
    elif motor == S4:
        if servo.getPosition(motor) == S4_INIT:
            return True
    else:
        print("   provided wrong input in isInDefaultPosition():robot.py 117")
        print("   argument: " + str(motor))

    return False

def setMotorOff(motor):
    if not inDefaultPosition(motor):
        for i in range(len(MOTORS)):
            if MOTORS[i] == motor: 
                servo.setTarget(MOTORS[i], DEFAULT_POSITIONS[i])
                break
            

def setMotorOn(motor):
    if not inDefaultPosition(motor):
        for i in range(len(MOTORS)):
            if MOTORS[i] == motor:
                servo.setTarget(MOTORS[i], ACTIVATED_POSITIONS[i])
                break

def setMotorsAcceleration(accel, list=MOTORS):
    for m in list:
        servo.setAccel(m, accel)

def parseAlgorithm(algorithm):
    algorithm = "R U R' R U R' U R U R' R U' R' U' R U R'"

