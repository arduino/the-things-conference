# This script allows to snap images and save them to the
# memory at a predefined interval. Those images can then be used 
# to train a machine learning model.

import sensor, image
from utime import sleep_ms

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_windowing([240,240])

counter = 0
label = "image"
while True:
    counter += 1

    # Records 48x48px images
    img = sensor.snapshot().copy(x_scale=0.201, y_scale=0.201)
    img.save("/%s_%d.jpg" % (label, counter), quality=100)
    sleep_ms(1000)
