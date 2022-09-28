# Edge Impulse - OpenMV Object Detection Example

import sensor, image, time, os, tf, math, uos, gc, machine

sensor.reset()                         # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)    # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)      # Set frame size to QVGA (320x240)
sensor.set_windowing((240, 240))       # Set 240x240 window.
sensor.skip_frames(time=2000)          # Let the camera adjust.

net = None
labels = None
min_confidence = 0.5

try:
    # Load built in model
    labels, net = tf.load_builtin_model('trained')
except Exception as e:
    raise Exception(e)

colors = [ # Add more colors if you are detecting more than 7 types of classes at once.
    (255,   0,   0),
    (  0, 255,   0),
    (255, 255,   0),
    (  0,   0, 255),
    (255,   0, 255),
    (  0, 255, 255),
    (255, 255, 255),
]

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

clock = time.clock()
while(True):
    clock.tick()

    img = sensor.snapshot()

    # detect() returns all objects found in the image (splitted out per class already)
    # we skip class index 0, as that is the background, and then draw circles of the center
    # of our objects

    insects = dict.fromkeys(labels, 0)

    for i, detection_list in enumerate(net.detect(img, thresholds=[(math.ceil(min_confidence * 255), 255)])):
        if (i == 0): continue # background class
        if (len(detection_list) == 0): continue # no detections for this class?
        filtered_distances = list(filter(lambda x: (x < 40), get_distances(detection_list)))
        insects[labels[i]] = len(detection_list) - len(filtered_distances)


        print("********** %s **********" % labels[i])
        for d in detection_list:
            [x, y, w, h] = d.rect()
            center_x = math.floor(x + (w / 2))
            center_y = math.floor(y + (h / 2))
            print('x %d\ty %d' % (center_x, center_y))
            img.draw_circle((center_x, center_y, 12), color=colors[i], thickness=2)

    print(insects)
    print(clock.fps(), "fps", end="\n\n")
