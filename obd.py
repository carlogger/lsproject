#!/usr/bin/python

# imports
# import obd
import board
import time
import digitalio
import random
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
        firstLine = "VSS: " + str(data[0]) + " mph"
        secondLine = "ESS: " + str(data[1]) + " RPM"
        thirdLine = "ET " + str(data[2]) + " F"
    elif mode == 1:
        firstLine = "TB: " + str(data[3]) + " PSI"
        secondLine = "IGM: " + str(data[4]) + " MPG"
        thirdLine = "OT: " + str(data[5]) + " F"
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

image = Image.new('1', (oled.width, oled.height))
draw = ImageDraw.Draw(image)
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)

currentMode = 0
maxMode = 1
leftJoyletgo = True
rightJoyletgo = True

while True:
    if !leftJoy.value and leftJoyletgo:
        currentMode = currentMode == 0 ? currentMode 
        

    displayOutput(0, retrieveOBD())

    time.sleep(1)
    
