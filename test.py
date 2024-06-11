import sys
import tensorflow as tf
import cv2
import numpy as np
import constants

if len(sys.argv) != 3:
    sys.exit("Usage: python test.py image model")

model = tf.keras.models.load_model(sys.argv[2])
image = cv2.imread(sys.argv[1], 0)
ret, image = cv2.threshold(image, 120, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
image = cv2.resize(image, (constants.IMG_WIDTH, constants.IMG_HEIGHT))

kernel = np.ones((3, 3), np.uint8)
# Hacer erode o dilate (random)

image = cv2.erode(image, kernel, iterations=1)

image = cv2.dilate(image, kernel, iterations=1)

classifications = None

classifications = model.predict(
    np.array(image).reshape(1, constants.IMG_WIDTH, constants.IMG_HEIGHT, 1)
)

if classifications is not None:
    for i in range(3):
        print(classifications.argmax(), constants.provincias[classifications.argmax()])
        classifications[0][np.argmax(classifications)] = 0

cv2.imshow("Matched image", image)
cv2.waitKey()
cv2.destroyAllWindows()
