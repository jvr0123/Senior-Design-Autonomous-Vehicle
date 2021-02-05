import time
import gpiozero as gpio
import pigpio
from PyQt5.QtCore import QThread

pi = pigpio.pi()

class MovementThread(QThread):
    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        def init(flag):
            # motors
            pi.set_mode(17, pigpio.OUTPUT)
            pi.set_mode(22, pigpio.OUTPUT)
            pi.set_mode(23, pigpio.OUTPUT)
            pi.set_mode(24, pigpio.OUTPUT)

            # servo
            # the bool flag decides whether we return none or an object for the servos
            if flag:
                pi.set_mode(4, pigpio.OUTPUT)
                pi.set_PWM_frequency(4, 50)

        def forward(sec):
            init(False)
            pi.write(17, 1)
            pi.write(22, 0)
            pi.write(23, 1)
            pi.write(24, 0)
            time.sleep(sec)

        def reverse(sec):
            init(False)
            pi.write(17, 0)
            pi.write(22, 1)
            pi.write(23, 0)
            pi.write(24, 1)
            time.sleep(sec)

        def turnRight(sec):
            servo1 = init(True)
            global duty
            if duty >= 2.6:
                duty = duty - 2.6
            servo1.ChangeDutyCycle(duty)
            time.sleep(sec)
            servo1.stop()
            gpio.cleanup()

        def turnLeft(sec):
            servo1 = init(True)
            global duty
            if duty <= 9.4:
                duty = duty + 2.6
            servo1.ChangeDutyCycle(duty)
            time.sleep(sec)
            servo1.stop()
            gpio.cleanup()

        def center(sec):
            servo1 = init(True)
            global duty
            duty = 6
            servo1.ChangeDutyCycle(duty)
            time.sleep(sec)
            servo1.stop()
            gpio.cleanup()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()
