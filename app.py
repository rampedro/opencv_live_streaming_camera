from flask import Flask, render_template, Response
import cv2

app = Flask(__name__)

camera = cv2.VideoCapture(0)  # use 0 for web camera
#  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera

import numpy as np
import pyzbar.pyzbar as pyzbar

font = cv2.FONT_HERSHEY_PLAIN

def gen_frames():  # generate frame by frame from camera
    go = True
    while go==True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            decodedObjects = pyzbar.decode(frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            #decodedObjects = pyzbar.decode(frame)
            for obj in decodedObjects:
                print(obj.data)
                go = False
                #cv2.putText(frame, str(obj.data), (50, 50), 2,font,(0, 255, 0), 3)
                break
    
                #yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + m + b'\r\n')  # concat frame one by one and show result
            #decodedObjects = pyzbar.decode(frame)
            #cv2.imshow("QR Scanner", frame)
            #camera.release()

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
