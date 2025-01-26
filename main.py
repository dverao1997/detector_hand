
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import cv2
from model.landmarks import DetectorManos
from utils.normalizar import Normalizar

# Inicializar el detector de manos
detector = DetectorManos(max_hands=1, detection_confidence=0.7, tracking_confidence=0.7)


archivo_csv = "lenguaje_senas.csv"


gestos_guardados = detector.cargar_gestos_guardados(archivo_csv)


# Capturar video de la cámara
cap = cv2.VideoCapture(0)

# Verificar si la cámara está activa
if not cap.isOpened():
    print("Error: No se pudo acceder a la cámara.")
    exit()

# Cargar una fuente compatible con Unicode
font_path = "arial.ttf"  # Cambia a la ruta de una fuente que tengas en tu sistema
font = ImageFont.truetype(font_path, 24)


# Verificar si el archivo existe y crearlo con las columnas si no


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Error: No se pudo leer el cuadro de la cámara.")
        break

    # Redimensionar y voltear el video
    frame = cv2.resize(frame, (640, 480))
    frame = cv2.flip(frame, 1)

    # Detectar manos
    results = detector.detect_landmarks(frame)
    
    landmarks = []
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mano = []
            for landmark in hand_landmarks.landmark:
                mano = [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]
            mano_normalizada = detector.normalizar_landmarks(mano)
            mano_escalada = detector.escalar_landmarks(mano_normalizada)
            distancias = detector.calcular_distancias(mano_escalada)
            landmarks.append(distancias)
        # print("Landmarks detectados:", landmarks) 

    # Mostrar mensaje si hay landmarks
    # if landmarks:
    #     gesto_detectado = "Mano detectada"
    #     mensaje_guardado = "Presiona 's' para guardar el gesto"
    # else:
    #     gesto_detectado = "No detectado"
    #     mensaje_guardado = ""

    if landmarks:
        gesto_reconocido = detector.comparar_gesto(landmarks[0], gestos_guardados)
        if gesto_reconocido:
            mensaje = f"Gesto detectado: {gesto_reconocido}"
        else:
            mensaje = "Gesto no reconocido"
    else:
        mensaje = "No se detecta ninguna mano o falta iluminación"

    # Convertir frame de OpenCV a formato PIL
    frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(frame_pil)
    
    # Mostrar el mensaje del gesto detectado
    # draw.text((10, 50), f"Gesto: {gesto_detectado}", font=font, fill=(0, 255, 0, 255))
    draw.text((10, 10), mensaje, font=font, fill=(0, 255, 0, 255))

    # Mostrar mensaje si no se detectan manos
    if not results.multi_hand_landmarks:
        draw.text((10, 10), "No se detecta ninguna mano o falta iluminación", font=font, fill=(255, 0, 0, 255))

    # Convertir de nuevo a formato OpenCV
    frame = cv2.cvtColor(np.array(frame_pil), cv2.COLOR_RGB2BGR)

    # Mostrar el video
    cv2.imshow("Deteccion de gestos", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('s') and landmarks:
        # Pedir el nombre del gesto por consola
        nombre_gesto = input("Introduce el nombre del gesto (letra o número): ")
        detector.guardar_gesto(nombre_gesto, mano_escalada, archivo_csv)
        print(f"Gesto '{nombre_gesto}' guardado exitosamente.")
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
