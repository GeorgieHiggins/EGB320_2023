import PiicoDev_VEML6040 as PiicoDev_VEML6040
import RPi.GPIO as GPIO
import time
import os

#Gripper
SG90_Pin = 33
#Scissor pins
ScissorA = 11
ScissorB = 15
#Ultrasonic
TRIG_PIN = 21
ECHO_PIN = 19

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(SG90_Pin,GPIO.OUT)
GPIO.setup(ScissorA, GPIO.OUT)
GPIO.setup(ScissorB, GPIO.OUT)
sensor = PiicoDev_VEML6040.PiicoDev_VEML6040()
SG90=GPIO.PWM(SG90_Pin,50)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

speed_sound = 34300



def get_distance():
    cycle_start = time.time()
    # Set trigger to HIGH
    pulse_end = 100000
    pulse_start = 100000
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    
    
    # Wait for echo to go HIGH
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()
        if (pulse_start - cycle_start) > 0.01:
            break

    # Wait for echo to go LOW
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    if pulse_end != 100000 and pulse_start != 100000:
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * speed_sound/2  # Speed of sound is 343 m/s
    else:
        distance = None

    return distance

detect = 0

def scissor_up():
    filter_distance = []
    global detect
    Avg_distance = 100000

    while detect !=2:
        edge = get_distance()
        
        if edge != None:

            if len(filter_distance) > 5:
                filter_distance.pop(0)
            
            filter_distance.append(edge)
            Avg_distance = sum(filter_distance)/len(filter_distance)

        if detect == 0:
            if Avg_distance < 6:
                GPIO.output(ScissorA,GPIO.HIGH)
                GPIO.output(ScissorB,GPIO.LOW)
                time.sleep(1)
            else:
                detect = 1
        elif detect == 1:
            if Avg_distance > 5.5:
                GPIO.output(ScissorA,GPIO.HIGH)
                GPIO.output(ScissorB,GPIO.LOW)
                time.sleep(1)
            else:
                detect = 2
        
    GPIO.output(ScissorA,GPIO.LOW)
    GPIO.output(ScissorB,GPIO.LOW)


def scissor_down(down_time):
    GPIO.output(ScissorA,GPIO.LOW)
    GPIO.output(ScissorB,GPIO.HIGH)
    time.sleep(1)
    edge = get_distance()
    if edge < 5:
        GPIO.output(ScissorA,GPIO.LOW)
        GPIO.output(ScissorB,GPIO.LOW)

def collection_loop(mobq, aisle_LR_q, action_q, height_q, last_q, complete):
    
    height = 100
    aisle_LR = 100
    SG90.start(0)
    
    while True:
        #print("Collection running waiting for queue")
        action = action_q.get(block=True)
        
        height = height_q.get(block=True)
        aisle_LR = aisle_LR_q.get(block=True)
        
        distance = get_distance()
        print(action, height, aisle_LR)
        
    
        filter_distance = []
        while True:
            
            distance = get_distance()

            if distance != None:
                if len(filter_distance) > 5:
                    filter_distance.pop(0)
                
                filter_distance.append(distance)
                Avg_distance = sum(filter_distance)/len(filter_distance)
                #print("Average:", Avg_distance, "Distance:", distance)
                if action=="Drop":
                    SG90.ChangeDutyCycle(11)
                    time.sleep(0.5)
                    complete.put(True)
                    break
                        #return to the queue "dropped"
                elif action=="Collect":
                
                    if Avg_distance > 6:
                        mobq.put("backward,55")
                        time.sleep(0.05)
                        mobq.put("stop,0")
                    elif Avg_distance > 5:
                        mobq.put("backward,45")
                        time.sleep(0.05)
                        mobq.put("stop,0")
                    else:
                        if height == 1:
                            scissor_up()
                            print("lift up successfully")
                        #searching
                        while True:
                            colours = sensor.readRGB()
                            red = colours['red']
                            green = colours['green']
                            blue = colours['blue']
                            
                            print(red, green, blue, "Detecting Orange")
                            
                            #detecting orange
                            #if red > 150 and green > 140 and blue > 91:
                            if red > 150 and green > 140 and blue > 84:
                                start = time.time()
                                print("Detect object")
                                break
                            if aisle_LR == "L":
                                mobq.put("left,60")
                                time.sleep(0.1)
                                mobq.put("stop,0")
                                time.sleep(0.1)
                                #print("panning right facing shelf")
                            elif aisle_LR == "R":
                                mobq.put("right,60")
                                time.sleep(0.1)
                                
                                #time.sleep(0.1)
                                mobq.put("stop,0")
                                time.sleep(0.1)
                                #print("panning left facing shelf")
                            else:
                                raise Exception("Invalid direction")

                        while True:
                            #detecting blue
                            colours = sensor.readRGB()
                            red = colours['red']
                            green = colours['green']
                            blue = colours['blue']
                            
                            print(red, green, blue, "Detecting blue")

                            if red < 150 and green < 160 and blue < 110:
                                end = time.time()
                                print("Shelve detected")
                                break
                            if aisle_LR == "L":
                                mobq.put("left,60")
                                time.sleep(0.1)
                                mobq.put("stop,0")
                                time.sleep(0.1)
                                #print("panning right facing shelf")
                            elif aisle_LR == "R":
                                mobq.put("right,60")
                                time.sleep(0.1)
                                mobq.put("stop,0")
                                time.sleep(0.1)
                                #print("panning left facing shelf")
                            else:
                                raise Exception("Invalid direction")
                        diff = end - start
                        print(diff)
                        mid = diff/7 #diff/2
                        if aisle_LR == "L":
                            mobq.put("right,60")
                            time.sleep(mid)
                            mobq.put("stop,0")
                            #print("panning left facing shelf")
                        elif aisle_LR == "R":
                            mobq.put("left,60")
                            time.sleep(mid)
                            mobq.put("stop,0")
                            #print("panning right facing shelf")
                        else:
                            raise Exception("Invalid direction")
                        
                        print("Collecting Item")
                        mobq.put("stop,0")
                        SG90.ChangeDutyCycle(2)
                        time.sleep(1.5)

                        complete.put(True)
                        break
                elif action=="Hold":
                    while True:
                        time.sleep(5)
                        if not action_q.empty():
                            action = action_q.get(block=False)
                            if action == "Drop":
                                distance = get_distance()
                                if distance != None:
                                    if len(filter_distance) > 5:
                                        filter_distance.pop(0)
                                    
                                    filter_distance.append(distance)
                                    Avg_distance = sum(filter_distance)/len(filter_distance)
                                    #print("Average:", Avg_distance, "Distance:", distance)
                                    
                                    if Avg_distance > 29:
                                        mobq.put("backward,65")
                                        time.sleep(0.05)
                                        mobq.put("stop,0")   
                                    elif Avg_distance > 24:
                                        mobq.put("backward,65")
                                        time.sleep(0.05)
                                        mobq.put("stop,0")  
                                    else:
                                        #drop the package
                                        SG90.ChangeDutyCycle(11)
                                        time.sleep(0.5)
                                        complete.put(True)
                                        break
