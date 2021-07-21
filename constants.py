import maestro
import time
servo = maestro.Controller('/dev/ttyAMA0')

M1 = 0  # gripper motor 1
M2 = 1  # gripper motor 2
M3 = 2  # gripper motor 3
M4 = 3  # gripper motor 4

S1 = 8  # slider motor 1
S2 = 9  # slider motor 1
S3 = 10 # slider motor 1
S4 = 11 # slider motor 1

M1_INIT = 3968  # gripper motor 1 default position
M2_INIT = 4200  # gripper motor 2 default position
M3_INIT = 4200  # gripper motor 3 default position
M4_INIT = 3968  # gripper motor 4 default position

M1_90 = 6600    # gripper motor 1 clockwise-rotated position
M2_90 = 6800    # gripper motor 2 clockwise-rotated position
M3_90 = 6900    # gripper motor 3 clockwise-rotated position
M4_90 = 6900    # gripper motor 4 clockwise-rotated position

S1_INIT = 3900  # slider motor 1 closed position
S2_INIT = 4600  # slider motor 2 closed position
S3_INIT = 4400  # slider motor 3 closed position
S4_INIT = 3900  # slider motor 4 closed position

S1_END = 9000  # slider motor 1 open position
S2_END = 9000  # slider motor 2 open position
S3_END = 9000  # slider motor 3 open position
S4_END = 9000  # slider motor 4 open position

NUM_MOTORS = 8

# arrays that hold all of the previous data in order for loop accessing
MOTORS = [M1, M2, M3, M4, S1, S2, S3, S4]
DEFAULT_POSITIONS = [M1_INIT, M2_INIT, M3_INIT, M4_INIT, S1_INIT, S2_INIT, S3_INIT, S4_INIT]
ACTIVATED_POSITIONS = [M1_90, M2_90, M3_90, M4_90, S1_END, S2_END, S3_END, S4_END]

ACCEL_SLOW = 30     # servo acceleration rate slow
ACCEL_NORMAL = 50   # servo acceleration rate normal

SLEEP = 0.4 # sleep value used inbetween different motor movements
SHORT = 0.1
MEDIUM = 0.2

def resetToDefault():
    print("Reseting to default positions")
    servo.setAccel(M1, ACCEL_NORMAL)
    servo.setAccel(S1, ACCEL_NORMAL)
    servo.setTarget(M1, M1_INIT)
    servo.setTarget(S1, S1_INIT)
    time.sleep(1)

    servo.setAccel(M2, ACCEL_NORMAL)
    servo.setAccel(S2, ACCEL_NORMAL)
    servo.setTarget(M2, M2_INIT)
    servo.setTarget(S2, S2_INIT)
    time.sleep(1)

    servo.setAccel(M3, ACCEL_NORMAL)
    servo.setAccel(S3, ACCEL_NORMAL)
    servo.setTarget(M3, M3_INIT)
    servo.setTarget(S3, S3_INIT)
    time.sleep(1)

    servo.setAccel(M4, ACCEL_NORMAL)
    servo.setAccel(S4, ACCEL_NORMAL)
    servo.setTarget(M4, M4_INIT)
    servo.setTarget(S4, S4_INIT)
    time.sleep(1)

def setToClosed():
    print("Setting to clsed position")

    step = 5

    increment1 = int((S1_END - S1_INIT)/step)
    increment2 = int((S2_END - S2_INIT)/step)
    increment3 = int((S3_END - S3_INIT)/step)
    increment4 = int((S4_END - S4_INIT)/step)

    a1 = int(S1_END)
    a2 = int(S2_END)
    a3 = int(S3_END)
    a4 = int(S4_END)

    servo.setTarget(M1, M1_INIT)
    servo.setTarget(M2, M2_INIT)
    servo.setTarget(M3, M3_INIT)
    servo.setTarget(M4, M4_INIT)

    for i in range(step):

        servo.setTarget(S2, a2)
        servo.setTarget(S4, a4)

        a2 -= increment2
        a4 -= increment4

        if i == step-1:
            servo.setTarget(S2, S2_INIT)
            servo.setTarget(S4, S4_INIT)

    time.sleep(1)

    for i in range(step):

        servo.setTarget(S1, a1)
        servo.setTarget(S3, a3)

        a1 -= increment1
        a3 -= increment3

        if i == step-1:
            servo.setTarget(S1, S1_INIT)
            servo.setTarget(S3, S3_INIT)

    print(a1)
    print(a2)
    print(a3)
    print(a4)


def setToOpen():
    print("Setting to open position")

    step = 5

    increment1 = int((S1_END - S1_INIT)/step)
    increment2 = int((S2_END - S2_INIT)/step)
    increment3 = int((S3_END - S3_INIT)/step)
    increment4 = int((S4_END - S4_INIT)/step)
    
    a1 = int(S1_INIT)
    a2 = int(S2_INIT)
    a3 = int(S3_INIT)
    a4 = int(S4_INIT)

    servo.setAccel(M1, ACCEL_SLOW)
    servo.setAccel(S1, ACCEL_SLOW)
    servo.setAccel(M2, ACCEL_SLOW)
    servo.setAccel(S2, ACCEL_SLOW)
    servo.setAccel(M3, ACCEL_SLOW)
    servo.setAccel(S3, ACCEL_SLOW)
    servo.setAccel(M4, ACCEL_SLOW)
    servo.setAccel(S4, ACCEL_SLOW)

    for i in range(step):
        servo.setTarget(S1, a1)
        servo.setTarget(S2, a2)
        servo.setTarget(S3, a3)
        servo.setTarget(S4, a4)

        a1 += increment1
        a2 += increment2
        a3 += increment3
        a4 += increment4

    servo.setTarget(M1, M1_INIT)
    servo.setTarget(M2, M2_INIT)
    servo.setTarget(M3, M3_INIT)
    servo.setTarget(M4, M4_INIT)

    print(a1)
    print(a2)
    print(a3)
    print(a4)

def tightenVertical():
    servo.setTarget(S1, S1_INIT-1000)
    servo.setTarget(S3, S3_INIT-1000)

def loosenVertical():
    servo.setTarget(S1, S1_INIT)
    servo.setTarget(S3, S3_INIT)

def tightenHorizontal():
    servo.setTarget(S2, S2_INIT-1000)
    servo.setTarget(S4, S4_INIT-1000)

def loosenHorizontal():
    servo.setTarget(S2, S2_INIT)
    servo.setTarget(S4, S4_INIT)
    
def acceptCube():
    time.sleep(2)
    setToOpen()
    time.sleep(SLEEP)
    setToClosed()
    time.sleep(SLEEP)
