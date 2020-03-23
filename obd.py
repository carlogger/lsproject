#!/usr/bin/python

# imports
# import obd
import board
import os
import time
from datetime import datetime
import digitalio
import random
import csv
from digitalio import DigitalInOut, Direction, Pull
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

def retrieveOBD():
    returnArray = []
    returnArray.append(random.randint(1,1000)) # engine runtime
    returnArray.append(random.randint(1,61)) # speed
    returnArray.append(random.randint(1000,4000)) # rpm
    returnArray.append(random.randint(185,195)) # temperature
    returnArray.append(random.randint(14,35)) # boost
    returnArray.append(random.randint(30,100)) # instant gas mileage
    returnArray.append(random.randint(170,185)) # oil temp
    return returnArray

def displayOutput(mode, data):
    if mode == 0:
        firstLine = "VSS: " + str(data[1]) + " mph"
        secondLine = "ESS: " + str(data[2]) + " RPM"
        thirdLine = "ET " + str(data[3]) + " F"
    elif mode == 1:
        firstLine = "TB: " + str(data[4]) + " PSI"
        secondLine = "IGM: " + str(data[5]) + " MPG"
        thirdLine = "OT: " + str(data[6]) + " F"
    elif mode == 2:
        firstLine = str(currentCar)
        secondLine = ""
        thirdLine = ""
    draw.rectangle((0, 0, oled.width, oled.height * 2), outline=0, fill=0)
    draw.text((0,0), firstLine, font=font, fill=255)
    draw.text((0,18), secondLine, font=font, fill=255)
    draw.text((0,36), thirdLine, font=font, fill=255)
    oled.image(image)
    oled.show()
        

# i2c interface and display
i2c = board.I2C()
RESET_PIN = digitalio.DigitalInOut(board.D4)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c, reset=RESET_PIN)

# button and joystick input
leftButton = DigitalInOut(board.D5)
leftButton.direction = Direction.INPUT
leftButton.pull = Pull.UP
 
rightButton = DigitalInOut(board.D6)
rightButton.direction = Direction.INPUT
rightButton.pull = Pull.UP
 
leftJoy = DigitalInOut(board.D27)
leftJoy.direction = Direction.INPUT
leftJoy.pull = Pull.UP
 
rightJoy = DigitalInOut(board.D23)
rightJoy.direction = Direction.INPUT
rightJoy.pull = Pull.UP
 
upJoy = DigitalInOut(board.D17)
upJoy.direction = Direction.INPUT
upJoy.pull = Pull.UP
 
downJoy = DigitalInOut(board.D22)
downJoy.direction = Direction.INPUT
downJoy.pull = Pull.UP
 
pressJoy = DigitalInOut(board.D4)
pressJoy.direction = Direction.INPUT
pressJoy.pull = Pull.UP

# enable connection to OBD-II
# connection = obd.OBD();

# Clear display
oled.fill(0)
oled.show()

# create image and font
image = Image.new('1', (oled.width, oled.height))
draw = ImageDraw.Draw(image)
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)

currentMode = 0
currentCar = 1
maxMode = 2
allLogs = []
leftJoyletgo = True
rightJoyletgo = True
rightButtonletgo = True
metric = False
secondsSinceEpoch = 0


while True:
    # if left joystick is pressed, change mode (decrease mode by 1)
    if not leftJoy.value and leftJoyletgo:
        currentMode = maxMode if currentMode == 0 else currentMode - 1
        displayOutput(currentMode, allLogs[-1])
        leftJoyletgo = False

    if leftJoy.value:
        leftJoyletgo = True

    # if right joystick is pressed, change mode (increase mode by 1)
    if not rightJoy.value and rightJoyletgo:
        currentMode = 0 if currentMode == maxMode else currentMode + 1
        displayOutput(currentMode, allLogs[-1])
        rightJoyletgo = False

    if rightJoy.value:
        rightJoyletgo = True

    # every second (without using sleep), update the logs and display data
    if secondsSinceEpoch != int(time.time()):
        allLogs.append(retrieveOBD())
        displayOutput(currentMode, allLogs[-1])
        secondsSinceEpoch = int(time.time())

    # if left button is pressed, save logs, upload logs, and exit
    if not leftButton.value:
        draw.rectangle((0, 0, oled.width, oled.height * 2), outline=0, fill=0)
        draw.text((0,0), "Saving logs ...", font=font, fill=255)
        oled.image(image)
        oled.show()

        if not os.path.exists("../logs"):
            os.makedirs("../logs")

        os.chdir("../logs")
        
        # if car directory doesn't exist, create it
        if not os.path.exists(str(currentCar)):
            os.makedirs(str(currentCar))

        # write to file
        with open(str(currentCar) + "/" + datetime.now().strftime("%Y%m%d%H%M%S.csv"), "w+") as my_csv:
            csvWriter = csv.writer(my_csv,delimiter=',')
            csvWriter.writerows(allLogs)
            
        draw.text((0,18), "Uploading logs ...", font=font, fill=255)
        oled.image(image)
        oled.show()
        # upload via git
        os.system("git add .")
        os.system("git commit -m 'auto commit'")
        os.system("git push origin master")
        draw.text((0,36), "Shutting down ...", font=font, fill=255)
        oled.image(image)
        oled.show()
        exit()

    if not rightButton.value and rightButtonletgo:
        currentCar = 1 if currentCar == 9 else currentCar + 1
        displayOutput(currentMode, allLogs[-1])
        rightButtonletgo = False

    if rightButton.value:
        rightButtonletgo = True
