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
