import cv2
import os

cam = cv2.VideoCapture(0)
path = "ImagesAttendance"

name = input("Enter Name:")

# cv2.nameWindow("Webcam")
img_counter = 0

# capturing frame (from camera)
while True:
    ret, frame = cam.read()

    if not ret:
        print("Failed to read frame")
        break
    
    # capturing frame and storing it in the database
    cv2.imshow(name+"(Press Space to capture.)", frame)

    k = cv2.waitKey(1)

    if k%256 == 27: # Esc key
        print("Escape hit, closing the app")
        exit()
    elif k%256 == 32: # Space key
        img_name = "{}.png".format(name)    # create image file
        cv2.imwrite(os. path. join(path , img_name), frame)
        print("Image Caputred")
        img_counter += 1
        cv2.putText(frame, "Hello World!!!", (200, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255))
        exit()



    cv2.waitKey(1)

# cam.release()

cam.destroyAllWindows()
