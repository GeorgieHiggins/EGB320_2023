import RPi.GPIO as GPIO
import time

# this servo motor uses 1ms pulse for 0 degree,
# 1.5ms for 90 degree
# 2ms for 180 degrees

# for 50Hz, on period is 20ms
# converting pulse to duty cycle...
# duty cycle % = (pulse ms/20)*100
# 0 degree = 5%
# 90 degree = 7.5%
# 180 degree = 10%

SG90_PIN = 33

GPIO.setmode(GPIO.BOARD)

GPIO.setup(SG90_PIN,GPIO.OUT)

SG90=GPIO.PWM(SG90_PIN,50)# 50hz frequency

SG90.start(0) # 2ms start pulse
time.sleep(0.5)
SG90.ChangeDutyCycle(11)
time.sleep(0.5)
SG90.stop()

GPIO.cleanup()