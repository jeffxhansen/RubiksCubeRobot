from constants import *

sleep = SLEEP

def shiftHorizontal():
    if (servo.getPosition(M2) != M2_INIT):
        servo.setTarget(M2, M2_INIT)
        time.sleep(1)

    servo.setTarget(S2, S2_END)
    time.sleep(sleep)
    servo.setTarget(M2, M2_90)
    time.sleep(sleep)
    servo.setTarget(S2, S2_INIT)
    time.sleep(sleep)

    if (servo.getPosition(M4) != M4_INIT):
        servo.setTarget(M4, M4_INIT)
        time.sleep(1)

    servo.setTarget(S4, S4_END)
    time.sleep(sleep)
    servo.setTarget(M4, M4_90)
    time.sleep(sleep)
    servo.setTarget(S4, S4_INIT)
    time.sleep(sleep)

def shiftHorizontalBack():

    tightenVertical()

    servo.setTarget(S2, S2_END)
    time.sleep(sleep)
    servo.setTarget(M2, M2_INIT)
    time.sleep(sleep)
    servo.setTarget(S2, S2_INIT)
    time.sleep(sleep)

    servo.setTarget(S4, S4_END)
    time.sleep(sleep)
    servo.setTarget(M4, M4_INIT)
    time.sleep(sleep)
    servo.setTarget(S4, S4_INIT)
    time.sleep(sleep)

    loosenVertical()

def rotate180(motor, slider, mInitial, sInitial, m90, sEnd):
    for i in range(2):
        if (servo.getPosition(motor) != mInitial):
            servo.setTarget(motor, mInitial)
            time.sleep(1)

        servo.setTarget(motor, m90)
        time.sleep(sleep)
        servo.setTarget(slider, sEnd)
        time.sleep(sleep)
        servo.setTarget(motor, mInitial)
        time.sleep(sleep)
        servo.setTarget(slider, sInitial)
        time.sleep(sleep)

def rotateCubeVertical():

    step = 5

    incrementTop = int((M1_90 - M1_INIT)/step)
    incrementBottom = int((M3_90 - M3_INIT)/step)

    top = int(M1_INIT)
    bottom = int(M3_90)

    servo.setAccel(M1, ACCEL_SLOW)
    servo.setAccel(S1, ACCEL_SLOW)
    servo.setAccel(M2, ACCEL_SLOW)
    servo.setAccel(S2, ACCEL_SLOW)
    servo.setAccel(M3, ACCEL_SLOW)
    servo.setAccel(S3, ACCEL_SLOW)
    servo.setAccel(M4, ACCEL_SLOW)
    servo.setAccel(S4, ACCEL_SLOW)

    tightenHorizontal()

    servo.setTarget(S1, S1_END)
    time.sleep(SLEEP)
    servo.setTarget(M1, M1_INIT)
    time.sleep(SLEEP)
    servo.setTarget(S1, S1_INIT)
    time.sleep(SLEEP)

    servo.setTarget(S3, S3_END)
    time.sleep(SLEEP)
    servo.setTarget(M3, M3_90)
    time.sleep(SLEEP)
    servo.setTarget(S3, S3_INIT)
    time.sleep(SLEEP)

    loosenHorizontal()

    servo.setTarget(S2, S2_END)
    servo.setTarget(S4, S4_END)
    time.sleep(SLEEP)

    for i in range(step):

        servo.setTarget(M1, top)
        servo.setTarget(M3, bottom)

        top += incrementTop
        bottom -= incrementBottom

        if i == step-1:
            servo.setTarget(M1, M1_90)
            servo.setTarget(M3, M3_INIT)

    servo.setTarget(S2, S2_INIT)
    servo.setTarget(S4, S4_INIT)
    time.sleep(SLEEP)

    tightenHorizontal()

    servo.setTarget(S1, S1_END)
    time.sleep(SLEEP)
    servo.setTarget(M1, M1_INIT)
    time.sleep(SLEEP)
    servo.setTarget(S1, S1_INIT)
    time.sleep(SLEEP)

    servo.setTarget(S3, S3_END)
    time.sleep(SLEEP)
    servo.setTarget(M3, M3_INIT)
    time.sleep(SLEEP)
    servo.setTarget(S3, S3_INIT)
    time.sleep(SLEEP)

    loosenHorizontal()

acceptCube()

time.sleep(1)

tightenVertical()

for i in range(2):
    if (servo.getPosition(M2) != M2_INIT):
        servo.setTarget(M2, M2_INIT)
        time.sleep(1)

    servo.setTarget(M2, M2_90)
    time.sleep(sleep)
    servo.setTarget(S2, S2_END)
    time.sleep(sleep)
    servo.setTarget(M2, M2_INIT)
    time.sleep(sleep)
    servo.setTarget(S2, S2_INIT)
    time.sleep(sleep)

for i in range(2):
    if (servo.getPosition(M4) != M4_INIT):
        servo.setTarget(M4, M4_INIT)
        time.sleep(1)

    servo.setTarget(M4, M4_90)
    time.sleep(sleep)
    servo.setTarget(S4, S4_END)
    time.sleep(sleep)
    servo.setTarget(M4, M4_INIT)
    time.sleep(sleep)
    servo.setTarget(S4, S4_INIT)
    time.sleep(sleep)

loosenVertical()

shiftHorizontal()
tightenHorizontal()

rotate180(M1, S1, M1_INIT, S1_INIT, M1_90, S1_END)
rotate180(M3, S3, M3_INIT, S3_INIT, M3_90, S3_END)

loosenHorizontal()

rotateCubeVertical()

tightenVertical()

shiftHorizontalBack()

rotate180(M2, S2, M2_INIT, S2_INIT, M2_90, S2_END)
rotate180(M4, S4, M4_INIT, S4_INIT, M4_90, S4_END)

setToOpen()
