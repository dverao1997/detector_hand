import cv2
from model.landmarks import DetectorManos
from view.main_window import MainWindow

class MainController:
    def __init__(self, root):
        self.root = root
        self.view = MainWindow(root)
        self.detector = DetectorManos()
        
        self.detector.entrenar_knn("lenguaje_senas.csv")
        
        self.view.boton_salir.config(command=self.cerrar)

        # Configurar captura de video
        self.cap = cv2.VideoCapture(0)
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.actualizar_video()

    def actualizar_video(self):
        """Captura frames de la cámara y los muestra en la ventana."""
        ret, frame = self.cap.read()
        frame = cv2.flip(frame, 1)
        if ret:
            # Detectar manos y procesar resultados
            results = self.detector.detect_landmarks(frame)
            landmarks = []
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mano = [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]
                    mano_normalizada = self.detector.normalizar_landmarks(mano)
                    mano_escalada = self.detector.escalar_landmarks(mano_normalizada)
                    distancias = self.detector.calcular_distancias(mano_escalada)
                    landmarks.append(distancias)

            # Reconocer gesto
            if landmarks:
                gesto_reconocido = self.detector.comparar_gesto(landmarks[0])
                if gesto_reconocido:
                    mensaje = f"Gesto detectado: {gesto_reconocido}"
                else:
                    mensaje = "Gesto no reconocido"
            else:
                mensaje = "No se detecta ninguna mano o falta iluminación"

            # Mostrar mensaje en pantalla
            self.view.mostrar_gesto(mensaje)

            # Convertir frame a RGB y mostrarlo en la ventana
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (640, 480))
            self.view.actualizar_video(frame)

        # Llamar a esta función nuevamente después de 10ms
        self.view.root.after(10, self.actualizar_video)

    def cerrar(self):
        print("Cerrando aplicación...")  # Confirmación en consola
        if hasattr(self, 'cap') and self.cap.isOpened():  # Verifica si la cámara está activa
            self.cap.release()  # Libera la cámara
        self.root.destroy()  # Cierra la ventana
