import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime


#  Getting Images and create List
path = 'Database'
images = []
classNames = []
myList = os.listdir(path)
# print(myList)

# Importing Images one by one
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

#Encoding faces
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

#Marking Attendance
def markAttendance(name):
    id=name
    dt_now = datetime.today()
    f_name = dt_now.strftime("%b-%d-%Y")
    open('Attendance/' + f_name + '.csv', 'a+')
    with open('Attendance/'+f_name+'.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if id not in nameList:
            detail = id.split('-')
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{id},{detail[0]},{dtString},{detail[1]}')


encodeListKnown = findEncodings(images)
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
            markAttendance(name)

    # Show webcam screen
    cv2.imshow('Face Recognition', img)
    cv2.waitKey(1)

