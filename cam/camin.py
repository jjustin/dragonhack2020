import numpy as np
import cv2
from time import sleep

fourcc = cv2.VideoWriter_fourcc(*'X264')
cap = cv2.VideoCapture(0)


def record(filename):
    input(filename)
    out = cv2.VideoWriter('videos/'+filename+".mp4", fourcc, 30,
                          (int(cap.get(3)), int(cap.get(4))))

    while True:
        ret, frame = cap.read()
        if ret == True:
            # write the flipped frame
            out.write(frame)

            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    out.release()


record("common")
record("test")
cap.release()
