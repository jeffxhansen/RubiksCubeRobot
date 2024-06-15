import sys
import os

x=[print(m) for m in sys.modules]
print(os.getcwd())

from pigpio_master import pigpio
pi = pigpio.pi()
pi.set_PWM_dutycycle(4, 20)