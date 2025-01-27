import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Reconocimiento de Gestos - Lenguaje de Señas")
        self.root.geometry("1290x800")
        self.root.resizable(False, False) 
        
        self.crear_widgets()
        
        # self.main_frame = tk.Frame(self.root, bg="white")
        # self.main_frame.pack()
        
        # self.title_frame = tk.Frame(self.main_frame, bg="red", height=50)
        # self.title_frame.pack(fill="x")

        # self.title_content = tk.Frame(self.title_frame, bg="red")
        # self.title_content.pack(expand=True)  # Centra el contenido dentro del marco principal

        # # Imagen en el título
        # self.logo_image = Image.open("logo.png")  # Cambia "logo.png" por el nombre de tu archivo
        
        # self.logo_image = self.logo_image.resize((300, 100), Image.Resampling.LANCZOS)
        
        # self.logo_tk = ImageTk.PhotoImage(self.logo_image)

        # self.logo_label = tk.Label(self.title_content, image=self.logo_tk, bg="red")
        # self.logo_label.pack(side="left", padx=10, pady=10)

        # # Contenedor 1 (izquierdo)
        # self.frame_detector = tk.Frame(self.main_frame, bg="blue", width=640, height=480)
        # self.frame_detector.pack(side="left", padx=5, pady=5)

        # # Contenedor 2 (derecho)
        # self.frame_camara = tk.Frame(self.main_frame, bg="green", width=640, height=480)
        # self.frame_camara.pack(side="left",padx=5, pady=5)
        # # # Título
        
        # # Gesto Detectado
        # self.label_gesto = tk.Label(self.root, text="Gesto detectado: Ninguno", font=("Arial", 12), bg="red", fg="white", width=50, height=2)
        # self.label_gesto.pack()

        # # Área para mostrar el video
        # self.video_frame = tk.Label(self.frame_camara, width=640, height=480)
        # self.video_frame.pack()

        # # Botón para salir
        # self.boton_salir = ttk.Button(self.root, text="Salir")
        # self.boton_salir.pack(pady=10)

    def actualizar_video(self, frame):
        """Actualiza el área de video con el frame proporcionado."""
        frame_tk = ImageTk.PhotoImage(Image.fromarray(frame))
        self.video_frame.config(image=frame_tk)
        self.video_frame.image = frame_tk

    def mostrar_gesto(self, gesto):
        """Muestra el nombre del gesto detectado."""
        self.label_gesto.delete("1.0", tk.END)  # Elimina el contenido actual del Text
        self.label_gesto.insert("1.0", f"{gesto}")  # Inserta el nuevo contenido


    def crear_widgets(self):
        self.imagen = Image.open("logo.png")
        self.imagen_resized = self.imagen.resize((150, 40))
        self.imagen_tk = ImageTk.PhotoImage(self.imagen_resized)
        
        self.imagen_inst = tk.Label(self.root, image=self.imagen_tk, bg="#60C1D0")
        self.imagen_inst.place(x=20, y=5)
        self.imagen_inst.image = self.imagen_tk
        
        self.titulo_texto = tk.Label(self.root, text="Traductor de texto", font=("Helvetica", 15, "bold"), bg='#FF9A4E')
        self.titulo_texto.place(x=20, y=55, width=200, height=40)
        
        
        self.asistente = tk.Label(self.root, text="Asistente", font=("Helvetica", 15, "bold"), bg='#FF9A4E')
        self.asistente.place(x=20, y=555, width=200, height=40)
        
        self.label_gesto = tk.Text(self.root, font=("Courier New", 20), wrap="word", width=20, height=5)
        self.label_gesto.place(x=20, y=100, width=300, height=200)
        
        self.frame_camara = tk.Frame(self.root, bg="green", width=640, height=480)
        self.frame_camara.place( x=350, y=100, width=640, height=480)

        self.video_frame = tk.Label(self.frame_camara, width=640, height=480, bg="black")
        self.video_frame.place( x=0, y=0, width=640, height=480)

        self.boton_salir = ttk.Button(self.root, text="Salir")
        self.boton_salir.place( x=20, y=700, width=100, height=40)