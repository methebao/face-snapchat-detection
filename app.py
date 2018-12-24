from flask import Flask, render_template, Response, request
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
import datetime

app = Flask(__name__)
face_cascade = cv2.CascadeClassifier("frontalface.xml")



def eye_aspect_ratio(eye):

	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])

	C = dist.euclidean(eye[0], eye[3])

	ear = (A + B) / (2.0 * C)

	return ear


print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

print("[INFO] starting video stream thread...")


@app.route('/')
def index():
    return render_template('index.html')

lineThickness = 2

def drawCat(frame,shape):
    cv2.line(frame, (shape[35][0], shape[35][1]), (shape[14][0], shape[14][1]), (0,255,0), lineThickness)
    cv2.line(frame, (shape[35][0], shape[35][1]), (shape[15][0], shape[15][1]), (0,255,0), lineThickness)
    cv2.line(frame, (shape[35][0], shape[35][1]), (shape[13][0], shape[13][1]), (0,255,0), lineThickness)

    cv2.line(frame, (shape[31][0], shape[31][1]), (shape[1][0], shape[1][1]), (0,255,0), lineThickness)
    cv2.line(frame, (shape[31][0], shape[31][1]), (shape[2][0], shape[2][1]), (0,255,0), lineThickness)
    cv2.line(frame, (shape[31][0], shape[31][1]), (shape[3][0], shape[3][1]), (0,255,0), lineThickness)
def drawGlass(frame,shape):
    cv2.circle(frame,(shape[36][0], shape[36][1]), 50, (0,255,0), 2)
    cv2.circle(frame,(shape[43][0], shape[43][1]), 50, (0,255,0), 2)
    cv2.line(frame, (shape[39][0], shape[39][1]), (shape[27][0], shape[27][1]), (0,255,0), lineThickness)
def gen(drawType, isRecording):
    print(drawType)
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    out = cv2.VideoWriter("./videos/video-"  + str(datetime.datetime.now()) + ".mp4", fourcc, 20.0, (640,480))

    start_time = time.time()
    print(start_time)
    print("----------------------------")
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: failed to capture image")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 0)
        for rect in rects:
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)

            ear = (leftEAR + rightEAR) / 2.0

            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
            if(drawType == "draw-cat"):
                drawCat(frame,shape)
            if(drawType == "draw-glass"):
                drawGlass(frame,shape)
            for (x, y) in shape:
                cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

        if (isRecording == 1):
            print("recording")
            # out.release()
            out.write(frame)
      
        cv2.imwrite('static/demo.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('static/demo.jpg', 'rb').read() + b'\r\n')


@app.route('/video_feed/<string:drawType>/<int:isRecording>')
def video_feed_record(drawType,isRecording):
    
    return Response(gen(drawType,isRecording),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feed/<string:drawType>')
def video_feed(drawType):
    return Response(gen(drawType,0),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/release')
def release():
    out.release()
    return "OK"

@app.route('/test')
def test():
   dict = {'phy':50,'che':60,'maths':70}
   return render_template('index.html', result = dict)

def test(): 
    return 
if __name__ == '__main__':
    app.run(debug=True)
