import cv2
import numpy as np
import face_recognition
import os
import attendance
import encode


#  Getting Images and create List
path = 'Database'
images = []
classNames = []
myList = os.listdir(path)

# Importing Images one by one
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

encodeListKnown = encode.faceEncodings(images)
print('Encoding Complete')

# Initializing webcam
capture = cv2.VideoCapture(0)

while True:
    success, img = capture.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

#     Finding all faces in our current frame
    facesCurrentFrame = face_recognition.face_locations(imgS)
#     Encoding of current frame
    encodeCurrentFrame = face_recognition.face_encodings(imgS,facesCurrentFrame)

#     Finding matches from the current frame
    for encodeFace,faceLocation in zip(encodeCurrentFrame,facesCurrentFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDistance = face_recognition.face_distance(encodeListKnown,encodeFace)
        print(faceDistance)
        matchingIndex = np.argmin(faceDistance)
#       Display name on the Image
        if matches[matchingIndex]:
            name = classNames[matchingIndex].upper()
            print(name)

#           Creating rectangle around faces
            y1,x2,y2,x1 = faceLocation
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,0.45,(255,255,255),1)
            attendance.markAttendance(name)

    # Show webcam screen
    cv2.imshow('Face Recognition', img)
    cv2.waitKey(1)

