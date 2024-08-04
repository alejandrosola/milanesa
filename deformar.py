import cv2
import numpy as np
import sys
import os
import random
import constants

NUM_CATEGORIES = 25

if len(sys.argv) != 2 and len(sys.argv) != 5:
    sys.exit("Usage: python deformar.py [images_path] [save_path] [iterations] [factors]")


def rotate_img(img, w, h):
    centro = (w // 2, h // 2)
    # Ángulo de rotación (por ejemplo, 45 grados)
    angle = random.randint(-45, 45)

    # Obtener la matriz de rotación
    M = cv2.getRotationMatrix2D(centro, angle, 1.0)

    # Realizar la rotación sin cambiar las dimensiones
    imagen_rotada = cv2.warpAffine(
        img,
        M,
        (w, h),
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(255, 255, 255),
    )
    return imagen_rotada

def def_img(img, w, ancho):
    base = int(w / 6)
    maxi = int(w / 3)
    inicio_x, inicio_y = random.randint(0, ancho - base), random.randint(
        0, alto - base
    )
    fin_x, fin_y = random.randint(
        inicio_x + base, inicio_x + base + maxi
    ), random.randint(inicio_y + base, inicio_y + base + maxi)
    mascara[inicio_y:fin_y, inicio_x:fin_x] = 255

    kernel = np.ones((3, 3), np.uint8)
    # Hacer erode o dilate (random)
    erosion = random.randint(0, 1)
    if erosion == 1:
        region_interes = cv2.erode(
            img[inicio_y:fin_y, inicio_x:fin_x], kernel, iterations=5
        )
    else:
        region_interes = cv2.dilate(
            img[inicio_y:fin_y, inicio_x:fin_x], kernel, iterations=5
        )

    # Combinar la región modificada con la imagen original
    img[inicio_y:fin_y, inicio_x:fin_x] = region_interes
    return img

def scale_img(imagen, scale_percent):
    original_height, original_width = imagen.shape

    # Calcula las nuevas dimensiones
    new_width = int(original_width * scale_percent / 100)
    new_height = int(original_height * scale_percent / 100)

    # Redimensiona la imagen
    resized_image = cv2.resize(imagen, (new_width, new_height))

    # Crea una nueva imagen con fondo blanco
    output_image = np.full(
        (original_height, original_width), 255, dtype=np.uint8
    )

    # Calcula las coordenadas para centrar la imagen redimensionada
    x_offset = (original_width - new_width) // 2
    y_offset = (original_height - new_height) // 2

    # Inserta la imagen redimensionada en el centro de la nueva imagen
    output_image[
        y_offset : y_offset + new_height, x_offset : x_offset + new_width
    ] = resized_image

    return output_image

data_dir = sys.argv[1]
cant_imagenes = int(sys.argv[3])

k = 0
for file in os.listdir(data_dir):
    print(k, file)
    # Cargar la imagen en blanco y negro
    image = cv2.imread(os.path.join(data_dir, file), 0)

    # Dimensiones originales
    original_height, original_width = image.shape

    # Dimensiones deseadas (constantes)
    target_width, target_height = constants.IMG_WIDTH, constants.IMG_HEIGHT

    # Calcula la relación de aspecto de la imagen original
    aspect_ratio = original_width / original_height

    # Calcula las nuevas dimensiones manteniendo la relación de aspecto
    if target_width / target_height > aspect_ratio:
        new_height = target_height
        new_width = int(target_height * aspect_ratio)
    else:
        new_width = target_width
        new_height = int(target_width / aspect_ratio)

    # Redimensiona la imagen
    resized_image = cv2.resize(image, (new_width, new_height))

    # Crea una nueva imagen con fondo blanco
    img = np.full((target_height, target_width), 255, dtype=np.uint8)

    # Calcula las coordenadas para centrar la imagen redimensionada
    x_offset = (target_width - new_width) // 2
    y_offset = (target_height - new_height) // 2

    # Inserta la imagen redimensionada en el centro de la nueva imagen
    img[y_offset : y_offset + new_height, x_offset : x_offset + new_width] = (
        resized_image
    )

    # Definir los puntos de referencia para la transformación
    alto, ancho = img.shape
    mascara = np.zeros((alto, ancho), dtype=np.uint8)
    factors = int(sys.argv[4])
    
    for i in range(cant_imagenes):
        output_image = img.copy()
        for j in range(random.randint(5, 15)):

            if factors >= 1:
                output_image = def_img(output_image, constants.IMG_WIDTH, ancho)

        if factors >= 2:
            output_image = rotate_img(
                output_image, constants.IMG_WIDTH, constants.IMG_HEIGHT
            )
        if factors >= 3:
            scale_percent = int(random.randint(40, 100))
            output_image = scale_img(output_image, scale_percent)

        if len(sys.argv) == 5:
            if not (
                os.path.exists(
                    os.path.join(sys.argv[2], str(constants.IMG_WIDTH), str(k))
                )
            ):
                os.makedirs(os.path.join(sys.argv[2], str(constants.IMG_WIDTH), str(k)))
            cv2.imwrite(
                os.path.join(
                    sys.argv[2], str(constants.IMG_WIDTH), str(k), str(i) + ".png"
                ),
                output_image,
            )
    k += 1

if len(sys.argv) == 4:
    print("Imágenes deformadas guardadas en " + sys.argv[2])
