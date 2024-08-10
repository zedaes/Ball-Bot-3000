import cv2
import numpy as np

class Camera:
    def __init__(self, cameraIndex=0):
        self.cameraIndex = cameraIndex
        self.cap = None

    def setup(self):
        self.cap = cv2.VideoCapture(self.cameraIndex)
        if not self.cap.isOpened():
            raise ValueError(f"Camera with index {self.cameraIndex} could not be opened.")

    def shutdown(self):
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()

    def getFrame(self):
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Failed to capture image from camera.")
        return frame

    def findOrangeBalls(self, frame):
        hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lowerOrange = np.array([5, 100, 100])
        upperOrange = np.array([15, 255, 255])
        mask = cv2.inRange(hsvFrame, lowerOrange, upperOrange)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        ballsPositions = []
        for contour in contours:
            ((x, y), radius) = cv2.minEnclosingCircle(contour)
            if radius > 5:
                ballsPositions.append((int(x), int(y), int(radius)))
        return ballsPositions, mask
