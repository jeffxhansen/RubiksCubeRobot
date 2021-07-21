import maestro
import time
servo = maestro.Controller('/dev/ttyAMA0')
i = 8
x = 0
time.sleep(3)
for j in range(4):
    print(str(i) + ": " + str(servo.getPosition(i)))
    print(str(x) + ": " + str(servo.getPosition(x)) + "\n")
    servo.setAccel(i, 50)
    servo.setTarget(i, 10000)
    print(str(i) + ": " + str(servo.getPosition(i)))
    print(str(x) + ": " + str(servo.getPosition(x)) + "\n")
    time.sleep(1)
    servo.setAccel(x, 50)
    servo.setTarget(x, 6800)
    print(str(i) + ": " + str(servo.getPosition(i)))
    print(str(x) + ": " + str(servo.getPosition(x)) + "\n")
    time.sleep(1)
    servo.setAccel(i, 50)
    servo.setTarget(i, 1000)
    print(str(i) + ": " + str(servo.getPosition(i)))
    print(str(x) + ": " + str(servo.getPosition(x)) + "\n")
    time.sleep(1)
    servo.setAccel(x, 50)
    servo.setTarget(x, 1000)
    print(str(i) + ": " + str(servo.getPosition(i)))
    print(str(x) + ": " + str(servo.getPosition(x)) + "\n")
    time.sleep(1)
    i += 1
    x += 1
servo.close
