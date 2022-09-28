import sensor, image, time, tf, pyb, math
from machine import Pin, SoftI2C
from utime import ticks_ms

host_address = 8
classification_interval = 2 * 1000
transmission_interval = 10 * 1000
min_confidence = 0.5
colors = [ # Add more colors if you are detecting more than 7 types of classes at once.
    (255,   0,   0),
    (  0, 255,   0),
    (255, 255,   0),
    (  0,   0, 255),
    (255,   0, 255),
    (  0, 255, 255),
    (255, 255, 255),
]

blueLED = pyb.LED(3) # built-in blue LED
i2c = SoftI2C(scl=Pin('I2C1_SCL') , sda=Pin('I2C1_SDA')) #I2C1
net = None
labels = None
lastcheck_transmission = None
lastcheck_classification = None
clock = time.clock()                # Create a clock object to track the FPS.
objects_info = []
sorted_counts = None

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
sensor.set_windowing((240, 240))       # Set 240x240 window.
sensor.skip_frames(time = 2000)     # Wait for settings take effect.


def send_result_to_host(counts, host_address):
    global i2c
    try:
        i2c.writeto(host_address, bytes(counts))
        return True
    except Exception as e:
        print(e)
        return False

def get_center(detection):
    [x, y, w, h] = detection.rect()
    center_x = math.floor(x + (w / 2))
    center_y = math.floor(y + (h / 2))
    return (center_x, center_y)

def get_distances(detection_list):
    distances = []
    for d in detection_list:
        d_center = get_center(d)
        for o in detection_list:
            if d == o: continue
            o_center = get_center(o)
            distances.append(math.sqrt(pow(o[0] - d[0], 2) + pow(o[1] - d[1], 2)))
    return distances

def get_insect_list(img, distance_threshold = 40):
    global colors
    global objects_info
    objects_info = []

    insects = dict.fromkeys(labels, 0)
    del insects['background']

    for i, detection_list in enumerate(net.detect(img, thresholds=[(math.ceil(min_confidence * 255), 255)])):
        if (i == 0): continue # background class
        if (len(detection_list) == 0): continue # no detections for this class?
        filtered_distances = list(filter(lambda d: (d < distance_threshold), get_distances(detection_list)))
        insects[labels[i]] = len(detection_list) - len(filtered_distances)

        #print("********** %s **********" % labels[i])
        for d in detection_list:
            [x, y, w, h] = d.rect()
            center_x = math.floor(x + (w / 2))
            center_y = math.floor(y + (h / 2))
            #print('x %d\ty %d' % (center_x, center_y))
            objects_info.append((center_x, center_y, colors[i]))
            #img.draw_circle((center_x, center_y, 12), color=colors[i], thickness=2)
    return insects

def draw_objects():
    for o in objects_info:
        img.draw_circle((o[0], o[1], 12), color=o[2], thickness=2)

def analyze_image(img):
    global host_address
    insects = get_insect_list(img)

    sorted_insects = sorted(insects.items())
    sorted_counts = list(map(lambda x: x[1], sorted_insects))
    print("---------------------------------------")
    print("Insects: %s" % sorted_insects)
    print("---------------------------------------\n")

    return sorted_counts

while(True):
    clock.tick()                    # Update the FPS clock.
    img = sensor.snapshot()         # Take a picture and return the image.
    img.gamma_corr(gamma=1.75, contrast=1.0, brightness=0.0)

    # Only run classification in a certain interval
    now = ticks_ms()
    should_analyze_image = lastcheck_classification == None or (now - lastcheck_classification) > classification_interval
    should_transmit_data = lastcheck_transmission == None or (now - lastcheck_transmission) > transmission_interval

    if (not lastcheck_classification or should_analyze_image):
        blueLED.on()
        sorted_counts = analyze_image(img)
        lastcheck_classification = now
        blueLED.off()

    if(not lastcheck_transmission or should_transmit_data):
        lastcheck_transmission = now
        if send_result_to_host(sorted_counts, host_address):
            print("Data sent successfully to host. ✅")
        else:
            print("Cloudn't send data to host. ❌")

    draw_objects()

    #print(clock.fps()) # Note: OpenMV Cam runs about half as fast when connected
                         # to the IDE. The FPS should increase once disconnected.
    #sensor.flush() # Flush latest image to IDE before sleeping
    #time.sleep(5) # Sleep for a bit to save energy
