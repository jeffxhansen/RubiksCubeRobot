import maestro
import time
servo = maestro.Controller('/dev/ttyAMA0')

motor1 = 1+8
motor2 = 3+8
servo.setAccel(motor1, 50)
servo.setAccel(motor2, 50)
a = servo.getPosition(motor1)
b = servo.getPosition(motor2)
for i in range(100):
    servo.setTarget(motor1, a)
    servo.setTarget(motor2, b)
    a += 10
    b += 10
    time.sleep(0.1)


