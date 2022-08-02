#!/usr/bin/env python3

import io
import time
import picamera # type: ignore # picamera is not installed on normal PCs

with picamera.PiCamera() as camera:
    # Set the camera's resolution to VGA @40fps and give it a couple
    # of seconds to measure exposure etc.
    camera.resolution = (640, 480)
    camera.framerate = 80
    time.sleep(2)
    # Set up 40 in-memory streams
    outputs = [io.BytesIO() for _ in range(40)]
    start = time.time()
    camera.capture_sequence(outputs, 'jpeg', use_video_port=True)
    finish = time.time()
    # How fast were we?
    print('Captured 40 images at %.2ffps' % (40 / (finish - start)))
