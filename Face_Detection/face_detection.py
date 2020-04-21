import cv2 as cv

original_image = cv.imread("image2.jpg")
grayscale_image = cv.cvtColor(original_image, cv.COLOR_BGR2GRAY)
face_cascade = cv.CascadeClassifier("haarcascade_frontalface_alt.xml")
detected_faces = face_cascade.detectMultiScale(grayscale_image, 1.3)


for (column, row, width, height) in detected_faces:
    cv.rectangle(
    original_image,
    (column, row),
    (column + width, row + height),
    (0,255,0),
    2
    )
# To display small image
small = cv.resize(original_image, (0,0), fx=0.3, fy=0.3)
cv.imshow('Face_Classifier', small)
# Use this for full size image
#cv.imshow('Image', original_image)
cv.waitKey(0)



########## Projekt ##############
"""Put the face recognizer into a class that can be easily used for different
use cases and rewrite the code for use in video"""
