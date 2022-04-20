import RPi.GPIO as GPIO

from MonitorTemperature import *
from constants import *


class PeltierModule:

    def __init__(self):
        self.currentCPUTemp = None
        self.in1 = IN1_PIN
        self.in2 = IN2_PIN
        self.ena = ENA_PIN
        self.setup_gpio()
        self.pwm = GPIO.PWM(self.ena, 1000)
        self.pwm.start(25)

    def setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        GPIO.setup(self.ena, GPIO.OUT)
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)

    def decide_action(self):
        temperature = MonitorTemperature()
        self.currentCPUTemp = temperature.get_current_temperature()
        if self.currentCPUTemp > MAX_TEMP - 15:
            self.very_hot()
        elif self.currentCPUTemp > MAX_TEMP - 5:

