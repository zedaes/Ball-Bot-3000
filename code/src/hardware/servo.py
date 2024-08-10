import RPi.GPIO as GPIO

class Servo:
    def __init__(self, pin, minPulse=500, maxPulse=2500):
        self.pin = pin
        self.minPulse = minPulse
        self.maxPulse = maxPulse
        self.isSetup = False

    def setup(self):
        if not self.isSetup:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.OUT)
            self.pwm = GPIO.PWM(self.pin, 50)
            self.pwm.start(0)
            self.isSetup = True

    def setAngle(self, angle):
        pulseWidth = self.minPulse + (angle / 180.0) * (self.maxPulse - self.minPulse)
        dutyCycle = pulseWidth / 20000.0 * 100
        self.pwm.ChangeDutyCycle(dutyCycle)

    def shutdown(self):
        if self.isSetup:
            self.pwm.stop()
            GPIO.cleanup()
            self.isSetup = False

    def checkup(self):
        passed = False
        try:
            if self.isSetup:
                return passed, f"Servo on pin {self.pin} is responsive."
            else:
                raise RuntimeError("Servo is not setup.")
        except Exception as e:
            return passed, f"Servo checkup failed: {e}"
