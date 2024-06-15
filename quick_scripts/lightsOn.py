from pigpio-master import pigpio
pi = pigpio.pi()
pi.set_PWM_dutycycle(4, 20)