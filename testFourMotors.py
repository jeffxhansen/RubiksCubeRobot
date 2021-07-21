import maestro
import time
servo = maestro.Controller('/dev/ttyAMA0')
for i in range(4):
    servo.setAccel(i,25)
    servo.setTarget(i,6000)
    time.sleep(2)
    servo.setAccel(i,25)
    servo.setTarget(i,1000)
    time.sleep(2)
servo.close
