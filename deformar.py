import cv2
import numpy as np
import sys
import os
import random
import constants

NUM_CATEGORIES = 25

if (len(sys.argv) != 2 and len(sys.argv) != 4):
    sys.exit("Usage: python deformar.py [images_path] [save_path] [iterations]")

data_dir = sys.argv[1]
cant_imagenes = int(sys.argv[3])

k = 0
for file in os.listdir(data_dir):
    # Cargar la imagen en blanco y negro
    img = cv2.imread(os.path.join(data_dir, file), 0)
    img = cv2.resize(img, (constants.IMG_WIDTH, constants.IMG_HEIGHT))

    # Definir los puntos de referencia para la transformación
    alto, ancho = img.shape
    mascara = np.zeros((alto, ancho), dtype=np.uint8)

    for i in range(cant_imagenes):
        imagen_deformada = img.copy()
        for j in range(random.randint(1, 2)):
            base = int(constants.IMG_WIDTH / 6)
            max = int(constants.IMG_WIDTH / 3)
            inicio_x, inicio_y = random.randint(0, ancho - base), random.randint(0, alto - base)
            fin_x, fin_y = random.randint(inicio_x + base, inicio_x + base + max), random.randint(inicio_y + base, inicio_y + base + max)
            mascara[inicio_y:fin_y, inicio_x:fin_x] = 255

            kernel = np.ones((3, 3), np.uint8)
            # Hacer erode o dilate (random)
            erosion = random.randint(0, 1)
            if (erosion == 1):
                region_interes = cv2.erode(img[inicio_y:fin_y, inicio_x:fin_x], kernel, iterations=2)
            else:
                region_interes = cv2.dilate(img[inicio_y:fin_y, inicio_x:fin_x], kernel, iterations=2)

            # Combinar la región modificada con la imagen original
            imagen_deformada[inicio_y:fin_y, inicio_x:fin_x] = region_interes

        if (len(sys.argv) == 4):
            if not (os.path.exists(os.path.join(sys.argv[2], str(k)))):
                os.makedirs(os.path.join(sys.argv[2], str(k)))
            cv2.imwrite(os.path.join(sys.argv[2], str(k),  str(i) + '.png'), imagen_deformada)
    k += 1

if (len(sys.argv) == 4):
    print("Imágenes deformadas guardadas en " + sys.argv[2])