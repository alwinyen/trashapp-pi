from pymongo import MongoClient
from pprint import pprint
import Adafruit_CharLCD as LCD
import requests
from io import BytesIO
from picamera import PiCamera
import RPi.GPIO as GPIO
import time
import random
import os

my_stream = BytesIO()
camera = PiCamera()

# Raspberry Pi pin setup
lcd_rs = 25
lcd_en = 24
lcd_d4 = 23
lcd_d5 = 17
lcd_d6 = 18
lcd_d7 = 22
lcd_backlight = 2

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2
start = False
stopCapture = False
imgCount = 0

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

# 16 Start
# 19, 13, 6 RGB Control
# 27, 26 NO
# 15, 20 YES
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(26, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)


client = MongoClient("mongodb+srv://guest:guest@cluster0-5sqr5.mongodb.net/test?retryWrites=true&w=majority")
db=client.admin

lcd.clear()


while True:
	if(start):
		imgCount = 0
		GPIO.output(6, GPIO.LOW)
		GPIO.output(19, GPIO.LOW)
		GPIO.output(13, GPIO.LOW)
		stopCapture = False
		lcd.clear()
		lcd.message('Press Green Btn\nTo Capture')
		GPIO.output(20, GPIO.HIGH)
		time.sleep(1)
		GPIO.output(20, GPIO.LOW)
		lcd.clear()
		lcd.message('Press Red Btn\nTo Discard')
		GPIO.output(26, GPIO.HIGH)
		time.sleep(1)
		GPIO.output(26, GPIO.LOW)
		lcd.clear()
		lcd.message('Press White Btn\nTo Send')
		GPIO.output(6, GPIO.HIGH)
		GPIO.output(19, GPIO.HIGH)
		GPIO.output(13, GPIO.HIGH)
		time.sleep(1)
		
		GPIO.output(20, GPIO.HIGH)
		GPIO.output(26, GPIO.HIGH)
		
		
		while(not stopCapture):
			time.sleep(0.5)
			if(GPIO.input(27)):
				imgCount = imgCount - 1 if imgCount > 0 else 0
				os.remove('img'+str(imgCount)+'.jpg')
				GPIO.output(26, GPIO.LOW)
				time.sleep(0.1)
				GPIO.output(26, GPIO.HIGH)
			
			if(GPIO.input(15)):
				camera.capture('img'+str(imgCount)+'.jpg')
				imgCount = imgCount + 1
				GPIO.output(20, GPIO.LOW)
				time.sleep(0.1)
				GPIO.output(20, GPIO.HIGH)
				
			if(GPIO.input(16)):
				lcd.clear()
				lcd.message('Thank You!\nRecycled '+ str(imgCount) + ' trash')
				time.sleep(2)
				if(imgCount > 0):
					lcd.clear()
					lcd.message('Type The Code\nOn Your App')
					time.sleep(3)
					lcd.clear()
					lcd.message(str(random.randint(100000,999999)))
					time.sleep(3)
				for x in range(imgCount):
					if os.path.isfile('img'+str(x)+'.jpg'):
						os.remove('img'+str(x)+'.jpg')
				start = False
				stopCapture = True
				
			lcd.clear()
			lcd.message('You have \n' + str(imgCount) + ' trash')
			time.sleep(0.1)
			
	else:
		lcd.clear()
		lcd.message('Press white \nbutton to start')
		GPIO.output(26, GPIO.LOW)
		GPIO.output(20, GPIO.LOW)
		GPIO.output(6, GPIO.HIGH)
		GPIO.output(19, GPIO.HIGH)
		GPIO.output(13, GPIO.HIGH)
		start = GPIO.input(16)
		time.sleep(0.5)



