from flask import Flask, render_template, Response
import cv2
import sys
import numpy
import time
import threading

app = Flask(__name__)
commonVideo = []
yesVideo = []
frameNum = 1

currentVideo = commonVideo


def process_file(filename, arr):
    print("Processing " + filename)
    file = cv2.VideoCapture(filename)
    while True:
        retval, im = file.read()
        if (retval == False):
            break
        imgencode = cv2.imencode('.jpg', im)[1]
        stringData = imgencode.tobytes()
        arr.append(stringData)
    del(file)
    print("Processed " + filename)


def gen_frames():
    inc = True
    while True:
        print(frameNum)
        time.sleep(1/30)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + currentVideo[frameNum] + b'\r\n')  # concat frame one by one and show result
        if inc:
            frameNum = frameNum + 1
            if frameNum >= len(currentVideo) - 4:
                inc = False
        else:
            frameNum = frameNum - 1
            if frameNum <= 2:
                inc = True


def switchToResponse():
    currentVideo = yesVideo


@app.route('/vid')
def vid():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# process loop video
t = threading.Thread(target=process_file, args=(
    "videos/common.mkv", commonVideo))
t.start()

# process respond message
t = threading.Thread(target=process_file, args=(
    "videos/test.mkv", yesVideo))
t.start()

app.run(host="0.0.0.0", port=5000, debug=True)
