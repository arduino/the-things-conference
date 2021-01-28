import sensor, image, time, os
from utime import sleep_ms
from lora_sender import LoraSender

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QVGA)
clock = time.clock()

#sender = LoraSender(interval=18000)
img_reader = image.ImageIO("/Traffic.bin", "r")
original_image = sensor.alloc_extra_fb(320, 240, sensor.GRAYSCALE)
background_image = sensor.alloc_extra_fb(320, 240, sensor.GRAYSCALE)
thresholds = (6, 255) # Define the grayscale range we're looking for

def print_blob_info(blob):
    vertical_position = blob.cy()
    if 140 <= vertical_position < 160:
        print("Direction: left")
    if 160 <= vertical_position < 190:
        print("Direction: right")
    print("Density: ", blob.density())
    print("Pixels: ", blob.pixels())
    print("Area: ", blob.area())
    print("Width: ", blob.w())
    print("Elongation: ", blob.elongation())
    print("-----------------")

# Use the first frame as background
for i in range(0, 10): # Or skip a few frames
    background_image.replace(img_reader.read(copy_to_fb=True, loop=True))

while(True):
    clock.tick() # Track elapsed milliseconds between snapshots().
    #sender.check() # Check for pending LoRa messages
    target_image = img_reader.read(copy_to_fb=True, loop=True)

    # Make a copy of the image
    original_image.replace(target_image)

    # Replace the image with the "abs(NEW-OLD)" frame difference.
    target_image.difference(background_image)

    # Find blobs
    blobs = target_image.find_blobs([thresholds], pixels_threshold=250, area_threshold=600, roi=(0,90,320,110), merge=True)

    # Comment out this line to see the diff image.
    target_image.replace(original_image)

    # Draw blobs
    for blob in blobs:
        target_image.draw_rectangle(blob.rect(), color=255)
        target_image.draw_cross(blob.cx(), blob.cy(), color=255)
        elongation = blob.elongation()

        if blob.area() > 5000 and elongation > 0.85:
            if 120 < blob.w() < 135:
                print("Bus detected!")
                #sender.replace_messages("Bus detected!")
            elif elongation > 0.9:
                print("Tram detected!")
                #sender.replace_messages("Tram detected!")
            else:
                continue
            print_blob_info(blob)

    # Set a value to create the desired frame rate
    sleep_ms(20)
    #print(clock.fps())

# Further considerations:
# - Track movement of blobs
# - Use image.get_histogram to detect patterns
# - Merge blobs only if certain parameters are met
# - Use more nuanced thresholds
# - Calcualte more complex directions using major_axis_line()
# - Detect congestion / rush hour
