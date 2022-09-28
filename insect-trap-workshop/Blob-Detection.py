import sensor, image, time, tf, pyb

# Define the min/max LAB values we're looking for
threshold_insects = (1, 40, -18, 45, -8, 40)
merged_blob_area_threshold = 600

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
#sensor.set_vflip(True) # Flips the image vertically
#sensor.set_hmirror(True) # Mirrors the image horizontally
sensor.skip_frames(time = 2000)     # Wait for settings take effect.

def find_blobs_in_image(img, blob_threshold):
    global merged_blob_area_threshold
    # Find blobs with a minimal area of 12x12 = 144 px
    # Overlapping blobs will be merged
    blobs = img.find_blobs([blob_threshold], invert=False, area_threshold=144, merge=True)
    # Skip blobs of small size after merging
    return list(filter(lambda b: (b.area() > merged_blob_area_threshold), blobs))

# Returns a 4 tuple representing a square (x,y,width,height)
# The square is created by using the longer side of the rectangle for both dimensions
def squareFromBlob(aBlob, margin = 30):
    if aBlob.w() > aBlob.h():
        largerSide = aBlob.w()
        newX = aBlob.x()
        newY = int(aBlob.y() - (largerSide - aBlob.h()) / 2)
    else:
        largerSide = aBlob.h()
        newX = int(aBlob.x() - (largerSide - aBlob.w()) / 2)
        newY = aBlob.y()

    half_margin = int(margin / 2)
    return (newX - half_margin, newY - half_margin, largerSide + margin, largerSide + margin)

def draw_blobs(blobs, img):
    for blob in blobs:
        # Draw a square where the blob was found
        img.draw_rectangle(squareFromBlob(blob), color=(0,255,0))
        #img.draw_rectangle(blob.rect(), color=(0,0,255))
        # Draw a cross in the middle of the blob
        img.draw_cross(blob.cx(), blob.cy(), color=(0,255,0))

while(True):
    #clock.tick()                    # Update the FPS clock.
    img = sensor.snapshot()         # Take a picture and return the image.
    img.gamma_corr(gamma=1.75, contrast=1.0, brightness=0.0)
    blobs = find_blobs_in_image(img, threshold_insects)
    draw_blobs(blobs, img)
