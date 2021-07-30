from flask import Flask, render_template, Response, request
import cv2
import numpy as np
from PIL import Image
import datetime, time
import os, sys
from threading import Thread
app=Flask(__name__)
camera = cv2.VideoCapture(0)


def thug():
    global capture 
    capture=0
    try:
        os.mkdir('./shots')
    except OSError as error:
        pass
    while True:
        success, image = camera.read()
        if not success:
            break
        else:
            maskPath = 'mask.png'

            harcasPath = 'haarcascade_frontalface_default.xml'

            faceCascade = cv2.CascadeClassifier(harcasPath)

            mask = Image.open(maskPath)

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            faces = faceCascade.detectMultiScale(gray, 2.1)

            background = Image.fromarray(image)

            for (x, y, w, h) in faces:
                resized_mask = mask.resize((w, h), Image.ANTIALIAS)

                offset = (x, y)
                background.paste(resized_mask, offset, mask=resized_mask)
    
            thug_filter = np.asarray(background)
            ret, buffer = cv2.imencode('.jpg', thug_filter)
            frame = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                   
            if(capture):
                capture=0
                now = datetime.datetime.now()
                p = os.path.sep.join(['shots', "shot_{}.png".format(str(now).replace(":",''))])
                cv2.imwrite(p, thug_filter)
            
            

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/video_feed')
def video_feed():
    return Response(thug(), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/requests',methods=['POST','GET'])
def tasks():
    global switch,camera
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture
            capture=1
    elif request.method=='GET':
        return render_template('index.html')
    return render_template('index.html')
if __name__=='__main__':
    app.run(debug=True)