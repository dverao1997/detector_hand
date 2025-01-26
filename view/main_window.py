import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Reconocimiento de Gestos - Lenguaje de Señas")
        self.root.geometry("800x800")

        # Título
        self.label_titulo = tk.Label(self.root, text="Reconocimiento de Gestos", font=("Arial", 24))
        self.label_titulo.pack(pady=10)

        # Gesto Detectado
        self.label_gesto = tk.Label(self.root, text="Gesto detectado: Ninguno", font=("Arial", 16))
        self.label_gesto.pack(pady=10)

        # Área para mostrar el video
        self.video_frame = tk.Label(self.root)
        self.video_frame.pack()

        # Botón para salir
        self.boton_salir = ttk.Button(self.root, text="Salir")
        self.boton_salir.pack(pady=10)

    def actualizar_video(self, frame):
        """Actualiza el área de video con el frame proporcionado."""
        frame_tk = ImageTk.PhotoImage(Image.fromarray(frame))
        self.video_frame.config(image=frame_tk)
        self.video_frame.image = frame_tk

    def mostrar_gesto(self, gesto):
        """Muestra el nombre del gesto detectado."""
        self.label_gesto.config(text=f"Gesto detectado: {gesto}")
