from tkinter import filedialog
import tensorflow as tf
import cv2
import numpy as np
import constants

from PIL import Image, ImageTk
import tkinter as tk


def open_file(window, variable):
    file_path = filedialog.askopenfilename()

    if not file_path:
        file_path = ""
    if variable == "model":
        window.model = file_path
    else:
        window.file = file_path
    print(file_path)
    return file_path


def query_ai(window, file, model):
    model = tf.keras.models.load_model(model)
    image = cv2.imread(file, 0)
    ret, image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    image = cv2.resize(image, (constants.IMG_WIDTH, constants.IMG_HEIGHT))

    kernel = np.ones((3, 3), np.uint8)

    # Erode y dilate para eliminar pixeles blancos en el medio de la mila
    image = cv2.erode(image, kernel, iterations=8)

    image = cv2.dilate(image, kernel, iterations=8)

    new_width, new_height = int(constants.IMG_WIDTH * 0.8), int(
        constants.IMG_HEIGHT * 0.8
    )
    original_height, original_width = constants.IMG_WIDTH, constants.IMG_HEIGHT

    resized_image = cv2.resize(image, (new_width, new_height))
    image = np.full((original_height, original_width), 255, dtype=np.uint8)

    x_offset = (original_width - new_width) // 2
    y_offset = (original_height - new_height) // 2

    # Inserta la imagen redimensionada en el centro de la nueva imagen
    image[y_offset : y_offset + new_height, x_offset : x_offset + new_width] = (
        resized_image
    )
    classifications = None

    classifications = model.predict(
        np.array(image).reshape(1, constants.IMG_WIDTH, constants.IMG_HEIGHT, 1)
    )

    cv2.imwrite("./test.jpg", image)

    window.create_img_window()
    window.img_window.deiconify()

    img = Image.open(file)
    img = img.resize((constants.IMG_WIDTH, constants.IMG_HEIGHT))
    img_tk = ImageTk.PhotoImage(img)

    frame1 = tk.Frame(window.img_window)
    frame1.pack(side=tk.LEFT, padx=50, pady=50)

    frame2 = tk.Frame(window.img_window)
    frame2.pack(side=tk.RIGHT, padx=50, pady=50)

    text1 = tk.Label(frame1, text="Tu milanesa")
    text1.pack()

    text2 = tk.Label(
        frame2, text=f"Resultado: {constants.provincias[classifications.argmax()]}"
    )
    text2.pack()

    res_img = Image.open(
        f"./resources/provincias/{constants.filenames[classifications.argmax()]}"
    )
    res_img = res_img.resize((constants.IMG_WIDTH, constants.IMG_HEIGHT))

    res_img_tk = ImageTk.PhotoImage(res_img)

    if classifications is not None:
        for i in range(3):
            print(
                classifications.argmax(), constants.provincias[classifications.argmax()]
            )
            classifications[0][np.argmax(classifications)] = 0

    res_label = tk.Label(frame2, image=res_img_tk)
    res_label.image = res_img_tk
    res_label.pack()

    label = tk.Label(frame1, image=img_tk)
    label.image = img_tk
    label.pack()
