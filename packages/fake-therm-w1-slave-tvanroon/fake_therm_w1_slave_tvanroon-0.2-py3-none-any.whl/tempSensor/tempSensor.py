import os
import random

class tempSensor:
    def __init__(self, min = 10000, max = 50000, outputDir = "", sensorNumber = ""):
       self.minTemp = self.testMinMax(min)
       self.maxTemp = self.testMinMax(max)
       self.outputDir = outputDir
       self.sensorNumber = sensorNumber
       self.temp = self.initTemp()
       self.rising = True

    def testMinMax(self, value):
        try:
            assert type(value) is int
            assert len(str(value)) == 5
            return value
        except AssertionError:
            print("min/max parameters must be integer with 5 digits")

    # set an initial temperature based on min/max temp set
    def initTemp(self):
        temp = random.randint(self.minTemp, self.maxTemp)
        return temp
    
    # rise and fall between min/max temp set
    def calculateTemp(self):
        if self.rising == True and self.temp < self.maxTemp:
            self.temp = self.temp + 100
        elif self.rising == True and self.temp > self.maxTemp:
            self.temp = self.temp - 100
            self.rising = False
        elif self.rising == False and self.temp > self.minTemp:
            self.temp = self.temp - 100
        elif self.rising == False and self.temp < self.minTemp:
            self.temp = self.temp + 100
            self.rising = True

    # create w1_slave file like in raspberry pi with GPIO
    def makeW1SlaveFile(self):
        foldername = "28-01204e9d2fa" + str(self.sensorNumber)
        outputFolder = os.path.join(self.outputDir, foldername)
        print(str(self.temp) + " written to: " + foldername)
        if not os.path.exists(outputFolder):
            os.makedirs(outputFolder)
        f = open(outputFolder + "/w1_slave", "w")
        f.write("17 01 4b 46 7f ff 0c 10 71 : crc=71 YES\n")
        f.write("17 01 4b 46 7f ff 0c 10 71 t=" + str(self.calculateTemp()))
        f.close()
        return