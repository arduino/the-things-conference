import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing(240, 240)
#sensor.set_vflip(True) # Flips the image vertically
#sensor.set_hmirror(True) # Mirrors the image horizontally
sensor.skip_frames(time = 2000)

clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot()
    img.gamma_corr(gamma=1.75, contrast=1.0, brightness=0.0)
    print(clock.fps())
