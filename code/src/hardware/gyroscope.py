import smbus2
import time

class Gyroscope:
    def __init__(self, bus=1, address=0x68):
        self.bus = smbus2.SMBus(bus)
        self.address = address
        self.isSetup = False

    def setup(self):
        if not self.isSetup:
            self.bus.write_byte_data(self.address, 0x6b, 0)
            self.isSetup = True

    def readRawData(self, addr):
        high = self.bus.read_byte_data(self.address, addr)
        low = self.bus.read_byte_data(self.address, addr + 1)
        value = (high << 8) + low
        if value > 32768:
            value -= 65536
        return value

    def getGyroData(self):
        gyroX = self.readRawData(0x43)
        gyroY = self.readRawData(0x45)
        gyroZ = self.readRawData(0x47)
        return gyroX, gyroY, gyroZ

    def getAccelData(self):
        accelX = self.readRawData(0x3b)
        accelY = self.readRawData(0x3d)
        accelZ = self.readRawData(0x3f)
        return accelX, accelY, accelZ

    def shutdown(self):
        if self.isSetup:
            self.bus.close()
            self.isSetup = False

    def checkup(self):
        passed = False
        try:
            if not self.isSetup:
                self.setup()

            gyroData = self.getGyroData()
            if all(data != 0 for data in gyroData):
                print(f"Gyroscope on address {self.address} is responsive.")
                return passed, "Gyroscope checkup successful."
            else:
                raise RuntimeError("Gyroscope data read returned zero values.")
        except Exception as e:
            return passed, f"Gyroscope checkup failed: {e}"
