# This script crops the camera window to a square format
# This is necessary for creating machine learning models which in 
# most cases only work on square images. That footage can then be used
# together with the frame-extractor.sh script to split the video into frames.
# Those frames can then be used to train a machine learning model.

import sensor, image

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.GRAYSCALE) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames(time = 1000)     # Wait for settings take effect.
sensor.set_windowing([240,240])     # Set windowing to square format for machine learning compatibility

while(True):
    img = sensor.snapshot()         # Take a picture and return the image.
