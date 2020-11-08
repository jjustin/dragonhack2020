from flask import Flask, send_from_directory, Response
import cv2
import sys
import numpy
import time
import threading
import subprocess
import asyncio
import websockets
import random

frame_time = 1/30
app = Flask(__name__)
commonVideo = []
yesVideo = []

currentVideo = commonVideo
frameNum = 1
ws_switch = False
inc = True
is_off = False


def process_file(filename, arr):
    print("Processing " + filename)
    file = cv2.VideoCapture(filename)
    while True:
        retval, im = file.read()
        if (retval == False):
            break
        imgencode = cv2.imencode('.jpg', im)[1]
        bytesData = imgencode.tobytes()
        arr.append(bytesData)
    del(file)
    print("Processed " + filename)


def gen_frames():
    global currentVideo
    global is_off
    while True:
        time.sleep(frame_time)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + get_next_frame() + b'\r\n')  # concat frame one by one and show result
        if is_off:
            yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + bytearray() + b'\r\n')  # concat frame one by one and show result
            is_off = False
            currentVideo  = commonVideo
            return ""


def get_next_frame():
    global frameNum
    if is_off:
        return bytearray()
    if (currentVideo == commonVideo):
        out = currentVideo[frameNum]
        inc_frame_num()
        return out

    xrand = random.randint(0, 10)
    if xrand == 0:
        xrand = random.random()
        frame_reduction = int(xrand * (1/frame_time))
        if (frameNum <= len(currentVideo) - 1 - frame_reduction):   # dont go out of bounds
            time.sleep(xrand)
            frameNum = frameNum + frame_reduction
            return currentVideo[frameNum]

    out = currentVideo[frameNum]
    # # randomize bytes on image
    # for i in range(0, len(currentVideo)-1):
    #     delta = random.randint(-currFrame[i], 255 - currFrame[i])
    #     out.append(currFrame[i] + delta)
    inc_frame_num()
    return out


def inc_frame_num():
    global inc
    global frameNum
    global is_off
    if inc:
        frameNum = frameNum + 1

        if frameNum >= len(currentVideo) - 4:
            if currentVideo != commonVideo:
                is_off = True
                print("sleepy boi")
                time.sleep(3)
                return
            inc = False
    else:
        frameNum = frameNum - 1
        if frameNum <= 2:
            inc = True


@ app.route('/switch')
def switch_to_response():
    global currentVideo
    global frameNum
    global ws_switch
    currentVideo = yesVideo
    frameNum = 1
    ws_switch = True
    return Response()

@app.route("/off")
def off():
    global is_off
    is_off = True



@ app.route('/vid')
def vid():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@ app.route('/aud')
def aud():
    def generate():
        with open('videos/test.mp4', 'rb') as file:
            file.seek(0)
            for chunk in iter(lambda: file.read(4096), b''):
                yield chunk
    return Response(generate(), mimetype='video/mp4')


@ app.route('/<path:path>')
def send_js(path):
    return send_from_directory('../videos', path)


async def echo(websocket, path):
    global ws_switch
    print("WS connected")
    while True:
        if (ws_switch):
            await websocket.send("switch")
            ws_switch = False
        time.sleep(0.1)


def start_ws():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.get_event_loop().run_until_complete(
        websockets.serve(echo, '0.0.0.0', 5001))
    asyncio.get_event_loop().run_forever()


def start():
    # process loop video
    t = threading.Thread(target=process_file, args=(
        "videos/common.mp4", commonVideo))
    t.start()

    # process respond message
    t = threading.Thread(target=process_file, args=(
        "videos/test.mp4", yesVideo))
    t.start()

    t = threading.Thread(target=start_ws)
    t.start()

    app.run(host="0.0.0.0", port=5000, debug=False)
