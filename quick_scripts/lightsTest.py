from pigpio-master import pigpio
from time import sleep
pi = pigpio.pi()

while True:
    for i in range(10,50):
        pi.set_PWM_dutycycle(4,i)
        sleep(0.005)
    for i in range(50, 9, -1):
        pi.set_PWM_dutycycle(4, i)
        sleep(0.005)
