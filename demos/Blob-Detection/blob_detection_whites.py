import pyb # Import module for board related functions
import sensor # Import the module for sensor related functions
import image # Import module containing machine vision algorithms
import time # Import module for tracking elapsed time

sensor.reset() # Resets the sensor
sensor.set_pixformat(sensor.GRAYSCALE) # Sets the sensor to grayscale
sensor.set_framesize(sensor.QVGA) # Sets the resolution to 320x240 px
sensor.skip_frames(time = 2000) # Skip some frames to let the image stabilize

thresholds = (220, 255) # Define the min/max gray scale values we're looking for
ledRed = pyb.LED(1) # Initiates the red led
ledGreen = pyb.LED(2) # Initiates the green led

clock = time.clock() # Instantiates a clock object

while(True):
    clock.tick() # Advances the clock
    img = sensor.snapshot() # Takes a snapshot and saves it in memory

    # Find blobs with a minimal area of 20x20 = 400 px
    # Overlapping blobs will be merged
    blobs = img.find_blobs([thresholds], area_threshold=400, merge=True)

    # Find blobs with a minimal amount of matching pixels of 2000 px
    # Overlapping blobs won't be merged
    #blobs = img.find_blobs([thresholds], pixels_threshold=2000, merge=False)

    # Draw blobs
    for blob in blobs:
        print("Density: ", blob.density())
        print("Pixels: ", blob.pixels())
        print("Area: ", blob.area())
        # Draw a rectangle where the blob was found
        img.draw_rectangle(blob.rect(), color=255)
        # Draw a cross in the middle of the blob
        img.draw_cross(blob.cx(), blob.cy(), color=0)

    # Turn on green LED if a blob was found
    if len(blobs) > 0:
        ledGreen.on()
        ledRed.off()
    else:
    # Turn the red LED on if no blob was found
        ledGreen.off()
        ledRed.on()

    #pyb.delay(50) # Pauses the execution for 50ms
    #print(clock.fps()) # Prints the framerate to the serial console
