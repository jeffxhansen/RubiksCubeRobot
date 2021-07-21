import maestro
import time
servo = maestro.Controller('/dev/ttyAMA0')

a = 0
b = 8

for i in range(4):
    servo.setAccel(a, 50)
    servo.setAccel(b, 50)
    servo.setTarget(a, 3968)
    servo.setTarget(b, 3968)
    time.sleep(1)
    a += 1
    b += 1
