import RPi.GPIO as GPIO
import time

# Set GPIO numbering mode to BOARD
GPIO.setmode(GPIO.BOARD)

# Define GPIO pins
TRIG_PIN = 40
ECHO_PIN = 37

# Set up GPIO pins
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

speed_sound = 34300
is_object = False
shelf_depth = 12

def get_distance():
    # Set trigger to HIGH
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)
    
    # Wait for echo to go HIGH
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    # Wait for echo to go LOW
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * speed_sound/2  # Speed of sound is 343 m/s

    return distance

try:
    distance = get_distance()
    print(distance)
    time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()
