from math import *
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
    def __init__(self, servos = [], motors = [], cameras = [], gyroscope = Gyroscope(), wheelRadius = 5, trackWidth = 10, startPose = Pose):
        self.completed = False
        self.alive = True

        self.wheelRadius = wheelRadius
        self.trackWidth = trackWidth

        self.pose = startPose

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
        ticksPerCount = self.frontLeftMotor.ticksPerCount

        frontLeftMotorTickCount = self.motors[0].tickCount
        frontRightMotorTickCount = self.motors[1].tickCount
        backLeftMotorTickCount = self.motors[2].tickCount
        backRightMotorTickCount = self.motors[3].tickCount

        for motor in self.motors:
            motor.updateTickCount()

        deltaFrontLeftMotorTickCount = frontLeftMotorTickCount - self.motors[0].tickCount
        deltaFrontRightMotorTickCount = frontRightMotorTickCount - self.motors[1].tickCount
        deltaBackLeftMotorTickCount = backLeftMotorTickCount - self.motors[2].tickCount
        deltaBackRightMotorTickCount = backRightMotorTickCount - self.motors[3].tickCount

        deltaFrontLeftDistance = (deltaFrontLeftMotorTickCount / ticksPerCount) * (2 * 3.14159 * self.wheelRadius)
        deltaFrontRightDistance = (deltaFrontRightMotorTickCount / ticksPerCount) * (2 * 3.14159 * self.wheelRadius)
        deltaBackLeftDistance = (deltaBackLeftMotorTickCount / ticksPerCount) * (2 * 3.14159 * self.wheelRadius)
        deltaBackRightDistance = (deltaBackRightMotorTickCount / ticksPerCount) * (2 * 3.14159 * self.wheelRadius)

        deltaFrontDistance = (deltaFrontLeftDistance + deltaFrontRightDistance) / 2
        deltaBackDistance = (deltaBackLeftDistance + deltaBackRightDistance) / 2

        deltaDistance = (deltaFrontDistance + deltaBackDistance) / 2
        deltaTheta = (deltaFrontRightDistance - deltaFrontLeftDistance) / self.trackWidth

        self.pose.x += deltaDistance * cos(self.theta + deltaTheta / 2)
        self.pose.y += deltaDistance * sin(self.theta + deltaTheta / 2)
        self.pose.heading += deltaTheta

        if self.theta > 3.14159:
            self.theta -= 2 * 3.14159
        elif self.theta < -3.14159:
            self.theta += 2 * 3.14159
