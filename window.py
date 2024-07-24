from tkinter import Tk, Button, Toplevel

from helpers import open_file, query_ai


class Window:
    def __init__(
        self,
        background="#1f1c1c",
    ):
        self.root = Tk()
        self.img_window = None
        self.create_img_window()
        self.root.geometry("300x200")

        self.file = "/home/alejandro/milanesa/resources/milanesas/dibujo0.png"
        self.model = "/home/alejandro/milanesa/models/modelo_rotadas.h5"

        self.root.config(background=background)

        self.root.title("Milanesas como provincias")

        self.select_file_button = Button(
            self.root,
            text="Seleccionar imágen",
            command=lambda: open_file(window=self, variable="file"),
        )
        self.select_file_button.pack(pady=20)

        self.select_model_button = Button(
            self.root,
            text="Seleccionar modelo",
            command=lambda: open_file(window=self, variable="model"),
        )
        self.select_model_button.pack(pady=20)

        self.query_ai_button = Button(
            self.root,
            text="Query",
            command=lambda: query_ai(window=self, file=self.file, model=self.model),
        )
        self.query_ai_button.pack(pady=20)

        self.root.mainloop()

    def create_img_window(self):
        # Si la ventana de imagen ya existe, solo la mostramos
        if self.img_window is not None:
            return

        # Crear una nueva ventana
        self.img_window = Toplevel(self.root)
        self.img_window.title("Resultado")
        self.img_window.withdraw()

        self.img_window.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        # Ocultar la ventana de imagen en lugar de destruirla
        self.img_window.withdraw()
        self.img_window = None
