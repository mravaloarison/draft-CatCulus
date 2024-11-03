import cv2
import dlib
import numpy as np

capture = cv2.VideoCapture(1)

detector = dlib.get_frontal_face_detector()

while True:
    ret, frame = capture.read()

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(frame)

    for face in faces:
        x, y = face.left(), face.top()
        x1, y1 = face.right(), face.bottom()

        cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

capture.release()