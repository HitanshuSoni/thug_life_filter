import cv2
import numpy as np
from PIL import Image

maskPath = 'mask.png'

harcasPath = 'haarcascade_frontalface_default.xml'

faceCascade = cv2.CascadeClassifier(harcasPath)

mask = Image.open(maskPath)

def thug_mask(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(gray, 2.1)

    background = Image.fromarray(image)

    for (x, y, w, h) in faces:
        resized_mask = mask.resize((w, h), Image.ANTIALIAS)

        offset = (x, y)
        background.paste(resized_mask, offset, mask=resized_mask)
    
    return np.asarray(background)

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()

    cv2.imshow("Thug Life Filter", thug_mask(frame))

    if cv2.waitKey(1) == 27:
        break

cap.release()

cv2.destroyAllWindows()