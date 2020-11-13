#!/usr/bin/env python3

import threading
import cv2
import numpy as np
import base64
import time
sem = threading.Semaphore()
exList = []
dspList = []

def extract():
    sem.acquire()

    # Initialize frame count
    count = 0

    # open video file
    vidcap = cv2.VideoCapture(clipFileName)

    # read first image
    success,image = vidcap.read()

    print("Reading frame {} {} ".format(count, success))
    while success:
        if len(exList) < 10:
            exList.append(image)

            success,image = vidcap.read()
            print('Reading frame {}'.format(count))
            count += 1
            # time.sleep(1)
            sem.release()
    print("Finished extracting all frames")
    sem.release()
def frameConvert():
    # initialize frame count
    sem.acquire()
    count = 0
    time.sleep(0.5)

    while len(exList) != 0:
        if len(exList) <= 10 and len(dspList) <= 10 and len(exList) != 0:
            print("Converting frame {}".format(count))

            # convert the image to grayscle
            grayscaleFrame = cv2.cvtColor(exList[0], cv2.COLOR_BGR2GRAY)

            exList.remove(exList[0])
            dspList.append(grayscaleFrame)

            count += 1
            # time.sleep(1)
            sem.release()
    print("Finished converting frames")
    sem.release()
def display():
    sem.acquire()
    frameDelay   = 42       
    time.sleep(1)
    # initialize frame count
    count = 0

    

    # load the frame
    frame = dspList[0]
    dspList.remove(dspList[0])

    while frame is not None:

        print("Displaying frame {}".format(count))
        # Display the frame in a window called "Video"
        cv2.imshow("Video", frame)

        


        # Wait for 42 ms and check if the user wants to quit
        if cv2.waitKey(42) and 0xFF == ord("q"):
            break

        
        # get the next frame filename
        count += 1

        # Read the next frame file
        if len(dspList) == 0:
            break

        frame = dspList[0]
        dspList.remove(dspList[0])

        sem.release()

    # make sure we cleanup the windows, otherwise we might end up with a mess
    print("Finished displaying all frames")
    cv2.destroyAllWindows()

clipFileName = "clip.mp4"

t1 = threading.Thread(target = extract).start()
t2 = threading.Thread(target = frameConvert).start()
t3 = threading.Thread(target = display).start()
