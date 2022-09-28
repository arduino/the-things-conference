import sensor, image, time, tf, pyb
from machine import Pin, SoftI2C
from utime import ticks_ms

# Define the min/max LAB values we're looking for
threshold_insects = (1, 40, -18, 45, -8, 40)
host_address = 8
merged_blob_area_threshold = 600
classification_interval = 5 * 1000

blueLED = pyb.LED(3) # built-in blue LED
i2c = SoftI2C(scl=Pin('I2C1_SCL') , sda=Pin('I2C1_SDA')) #I2C1
net = None
labels = None
lastcheck = None
clock = time.clock()                # Create a clock object to track the FPS.

try:
    # Load built in model
    labels, net = tf.load_builtin_model('trained')
except Exception as e:
    raise Exception(e)

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
#sensor.set_vflip(True) # Flips the image vertically
#sensor.set_hmirror(True) # Mirrors the image horizontally
sensor.skip_frames(time = 2000)     # Wait for settings take effect.


def classifyImage(img, roi, confidence_threshold = 0.65):
    # default settings just do one detection... change them to search the image...
    for obj in net.classify(img, roi=roi, min_scale=1.0, scale_mul=0.8, x_overlap=0.5, y_overlap=0.5):
        print("**********\nPredictions at [x=%d,y=%d,w=%d,h=%d]" % obj.rect())
        #img.draw_rectangle(obj.rect())
        # This combines the labels and confidence values into a list of tuples
        confidences = obj.output()
        predictions_list = list(zip(labels, confidences))

        for i in range(len(predictions_list)):
            print("%s = %f" % (predictions_list[i][0], predictions_list[i][1]))

        highest_confidence = max(confidences)
        most_promising_item = predictions_list[confidences.index(highest_confidence)][0]
        #print("Highest confidence: %f" % highest_confidence)
        #print("Most promising item: %s" % most_promising_item)
        return most_promising_item if highest_confidence > confidence_threshold else None

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

def send_result_to_host(counts, host_address):
    global i2c
    try:
        i2c.writeto(host_address, bytes(counts))
        return True
    except Exception as e:
        print(e)
        return False

def analyze_blobs(blobs, img):
    global host_address
    insects = dict.fromkeys(labels, 0)

    for blob in blobs:
        #print(blob) # For debugging
        roi = squareFromBlob(blob)
        insect = classifyImage(img, roi)

        if insect == None: continue
        print("'%s' spotted 🕵️‍" % insect)
        insects[insect] += 1

    sorted_insects = sorted(insects.items())
    sorted_counts = list(map(lambda x: x[1], sorted_insects))
    print("---------------------------------------")
    print("Insects: %s" % sorted_insects)
    print("---------------------------------------\n")

    if send_result_to_host(sorted_counts, host_address):
        print("Data sent successfully to host. ✅")
    else:
        print("Cloudn't send data to host. ❌")

while(True):
    clock.tick()                    # Update the FPS clock.
    img = sensor.snapshot()         # Take a picture and return the image.
    img.gamma_corr(gamma=1.75, contrast=1.0, brightness=0.0)
    blobs = find_blobs_in_image(img, threshold_insects)

    # Enable if not drawn by classification function
    draw_blobs(blobs, img)

    # Only run classification in a certain interval
    now = ticks_ms()
    should_analyze_blobs = lastcheck == None or (now - lastcheck) > classification_interval

    if (not lastcheck or should_analyze_blobs):
        blueLED.on()
        analyze_blobs(blobs, img)
        lastcheck = now
        blueLED.off()

    #print(clock.fps()) # Note: OpenMV Cam runs about half as fast when connected
                         # to the IDE. The FPS should increase once disconnected.
    #sensor.flush() # Flush latest image to IDE before sleeping
    #time.sleep(5) # Sleep for a bit to save energy
