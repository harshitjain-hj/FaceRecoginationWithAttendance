import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

# from PIL import ImageGrab
#  Getting Images and create List
path = 'ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
print(myList)

# Importin Images one by one
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)
# Encoding faces
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

#   Marking Attendance
def markAttendance(name):
    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        # fetch data from list one by one
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        #     Check whether name is in the list or not
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')

# markAttendance('Rahul Singh')
# #### FOR CAPTURING SCREEN RATHER THAN WEBCAM
# # def captureScreen(bbox=(300,300,690+300,530+300)):
# #     capScr = np.array(ImageGrab.grab(bbox))
# #     capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
# #     return capScr
#
encodeListKnown = findEncodings(images)
print('Encoding Complete')

# Initializing webcam
capture = cv2.VideoCapture(0)
#
while True:
    success, img = capture.read()
    #img = captureScreen()
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
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            markAttendance(name)

    # Show webcam screen
    cv2.imshow('Webcam',img)
    cv2.waitKey(1)
