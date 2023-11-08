import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

#Define GPIO pins
A1A = 11
A1B = 15

SG90_PIN = 33

GPIO.setup(SG90_PIN,GPIO.OUT)

SG90=GPIO.PWM(SG90_PIN,50)

SG90.start(0) # 2ms start pulse
time.sleep(0.5)
SG90.ChangeDutyCycle(11)
time.sleep(0.5)

GPIO.setup(A1A, GPIO.OUT)
GPIO.setup(A1B, GPIO.OUT)
GPIO.output(A1A,GPIO.HIGH)
GPIO.output(A1B,GPIO.LOW)

#12 seconds for middle shelf
time.sleep(3)
GPIO.cleanup()
