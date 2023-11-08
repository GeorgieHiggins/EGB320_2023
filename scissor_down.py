import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

#Define GPIO pins
A1A = 11
A1B = 15

GPIO.setup(A1A, GPIO.OUT)
GPIO.setup(A1B, GPIO.OUT)
GPIO.output(A1A,GPIO.LOW)
GPIO.output(A1B,GPIO.HIGH)

time.sleep(2)
GPIO.cleanup()
