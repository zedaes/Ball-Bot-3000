import RPi.GPIO as GPIO
import time

class StepperMotor:
    def __init__(self, stepPin, directionPin, enablePin=None, stepsPerRevolution=200):
        self.stepPin = stepPin
        self.directionPin = directionPin
        self.enablePin = enablePin
        self.stepsPerRevolution = stepsPerRevolution
        self.tickCount = 0
        self.isSetup = False

    def setup(self):
        if not self.isSetup:
            GPIO.setmode(GPIO.BCM)
            self.setupPin(self.stepPin)
            self.setupPin(self.directionPin)
            if self.enablePin:
                self.setupPin(self.enablePin)
                self.enable()
            self.tickCount = 0
            self.isSetup = True

    def setupPin(self, pin):
        GPIO.setup(pin, GPIO.OUT)

    def pulseStepPin(self, delay):
        GPIO.output(self.stepPin, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(self.stepPin, GPIO.LOW)
        time.sleep(delay)

    def step(self, steps, direction=GPIO.HIGH, delay=0.001):
        if not self.isSetup:
            self.setup()

        direction_value = GPIO.HIGH if direction else GPIO.LOW
        GPIO.output(self.directionPin, direction_value)
        for step in range(steps):
            self.pulseStepPin(delay)
            self.updateTickCount(direction_value)


    def updateTickCount(self, direction):
        if direction == GPIO.HIGH:
            self.tickCount += 1
        else:
            self.tickCount -= 1

    def getTicks(self):
        return self.tickCount

    def enable(self):
        if self.enablePin:
            GPIO.output(self.enablePin, GPIO.LOW)

    def disable(self):
        if self.enablePin:
            GPIO.output(self.enablePin, GPIO.HIGH)

    def shutdown(self):
        self.disable()
        self.cleanup()

    def cleanup(self):
        if self.isSetup:
            GPIO.cleanup()
            self.isSetup = False
