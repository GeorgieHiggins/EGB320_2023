import PiicoDev_VEML6040 as PiicoDev_VEML6040
import time

sensor = PiicoDev_VEML6040.PiicoDev_VEML6040()
#for orange: r_thresh > 150, g_thresh > 140, b_thresh > 91
#for blue: 125 < r_thresh, 129 < g_thresh < 131, b_thresh < 91
"""
while True:
    colours = sensor.readRGB()
    print(colours)
    time.sleep(0.5)
"""

while True:
    colours = sensor.readRGB()
    red = colours['red']
    blue = colours['blue']
    green = colours['green']
    print(colours)
    if red > 200 and green > 129:
        print("orange")
    elif red < 150 and blue < 91:
        print("blue")
    else:
        print("other")
    
    time.sleep(0.5)

"""
while True:
    colours = sensor.readRGB()
    red = colours['red']
    green = colours['green']
    blue = colours['blue']
    #detecting orange
    if red > 150 and green > 140 and blue > 91:
        start = time.time()
        break
    time.sleep(0.25)

while True:
    #detecting blue
    if red > 125 and green > 129 and green < 131 and blue < 91:
        end = time.time()
        break
    time.sleep(0.25)

diff = end - start
mid = diff/2
print(mid)
"""