import math
from code.src.hardware import gyroscope
import cv2

from hardware.camera import *
from hardware.gyroscope import *
from hardware.motor import *
from hardware.servo import *
from odometry.motionSequence import *
from odometry.pose import *
from vision.detection import *



class Robot:
    def __init__(self, servos = [], motors = [], cameras = [], gyroscope = Gyroscope()):
        self.completed = False
        self.alive = True

        self.report = None

        self.baseServo = servos[0]
        self.shoulderServo = servos[1]
        self.elbowServo = servos[2]
        self.wristServo = servos[3]
        self.clawServo = servos[4]

        self.frontLeftMotor = motors[0]
        self.frontRightMotor = motors[1]
        self.backLeftMotor = motors[2]
        self.backRightMotor = motors[3]

        self.leftCamera = cameras[0]
        self.rightCamera = cameras[1]

        self.gyroscrope = gyroscope

        self.servos = [self.baseServo, self.shoulderServo, self.elbowServo, self.wristServo, self.clawServo]
        self.motors = [self.frontLeftMotor, self.frontRightMotor, self.backLeftMotor, self.backRightMotor]
        self.cameras = [self.leftCamera, self.rightCamera]

        self.hardware = [self.baseServo, self.shoulderServo, self.elbowServo, self.wristServo, self.clawServo, self.frontLeftMotor, self.frontRightMotor, self.backLeftMotor, self.backRightMotor, self.leftCamera, self.rightCamera]

    def main(self):
        if not self.alive:
            self.shutdown

    def shutdown(self):
        for hardware in self.hardware:
            hardware.shutdown()

        print(self.report)

    def setup(self):
        for hardware in self.hardware:
            hardware.setup()

        self.checkup()

    def checkup(self):
        for hardware in self.hardware:
            hardware.checkup()

    def updatePose(self):
        for motor in self.motors:
            motor.updateTickCount()
