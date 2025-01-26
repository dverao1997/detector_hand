import mediapipe as mp
import csv
import os
import numpy as np

class DetectorManos:
    def __init__(self, max_hands=1, detection_confidence=0.7, tracking_confidence=0.7):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.mp_drawing = mp.solutions.drawing_utils

    def detect_landmarks(self, frame):
        results = self.hands.process(frame)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )
        return results
        
    # def guardar_gesto(self, nombre_gesto, landmarks, archivo_csv):
    #     """Guarda un nuevo gesto en el archivo CSV."""
    #     try:
    #         # Verificar si el archivo existe y crearlo con columnas si no
    #         if not os.path.exists(archivo_csv):
    #             with open(archivo_csv, mode='w', newline='') as file:
    #                 escritor_csv = csv.writer(file)
    #                 # Escribir columnas del archivo
    #                 columnas = ['nombre_gesto'] + [f'x{i},y{i},z{i}' for i in range(21)]
    #                 escritor_csv.writerow(columnas)
    #             print(f"Archivo {archivo_csv} creado con columnas.")

    #         # Abrir el archivo en modo apéndice para escribir una nueva fila
    #         with open(archivo_csv, mode='a', newline='') as file:
    #             escritor_csv = csv.writer(file)
    #             # Crear la fila con el nombre del gesto y las coordenadas
    #             fila = [nombre_gesto] + [coord for punto in landmarks for coord in punto]
    #             print(f"Fila a guardar: {fila}")  # Verificar la fila
    #             escritor_csv.writerow(fila)  # Escribir la fila
    #         print(f"Gesto '{nombre_gesto}' guardado exitosamente en {archivo_csv}.")
    #     except Exception as e:
    #         print(f"Error al guardar el gesto: {e}")
    
    
    def guardar_gesto(self, nombre_gesto, landmarks, archivo_csv):
        """Guarda un nuevo gesto en el archivo CSV."""
        try:
            # Calcular distancias antes de guardar
            distancias = self.calcular_distancias(landmarks)

            # Verificar si el archivo existe y crearlo con columnas si no
            if not os.path.exists(archivo_csv):
                with open(archivo_csv, mode='w', newline='') as file:
                    escritor_csv = csv.writer(file)
                    # Escribir columnas del archivo
                    columnas = ['nombre_gesto'] + [f'distancia_{i}' for i in range(len(distancias))]
                    escritor_csv.writerow(columnas)
                print(f"Archivo {archivo_csv} creado con columnas.")

            # Abrir el archivo en modo apéndice para escribir una nueva fila
            with open(archivo_csv, mode='a', newline='') as file:
                escritor_csv = csv.writer(file)
                # Crear la fila con el nombre del gesto y las distancias
                fila = [nombre_gesto] + distancias
                escritor_csv.writerow(fila)  # Escribir la fila
            print(f"Gesto '{nombre_gesto}' guardado exitosamente en {archivo_csv}.")
        except Exception as e:
            print(f"Error al guardar el gesto: {e}")

            
    def normalizar_landmarks(self, landmarks):
        """Normaliza los landmarks para que sean relativos a la base de la palma."""
        base_x, base_y, base_z = landmarks[0]
        landmarks_normalizados = [(x - base_x, y - base_y, z - base_z) for x, y, z in landmarks]
        return landmarks_normalizados

    def escalar_landmarks(self, landmarks):
        """Escala los landmarks para que estén en un rango uniforme."""
        max_val = max(max(abs(x), abs(y), abs(z)) for x, y, z in landmarks)
        landmarks_escalados = [(x / max_val, y / max_val, z / max_val) for x, y, z in landmarks]
        return landmarks_escalados

    def calcular_distancias(self, landmarks):
        """Calcula las distancias entre cada par de landmarks."""
        distancias = []
        for i in range(len(landmarks)):
            for j in range(i + 1, len(landmarks)):
                distancias.append(np.linalg.norm(np.array(landmarks[i]) - np.array(landmarks[j])))
        return distancias
    


    def cargar_gestos_guardados(self,archivo_csv):
        """Carga los gestos guardados en un archivo CSV y devuelve una lista de gestos y sus distancias."""
        
        gestos = []
        with open(archivo_csv, mode='r') as file:
            lector_csv = csv.reader(file)
            next(lector_csv)  # Saltar la fila de encabezado
            for fila in lector_csv:
                nombre_gesto = fila[0]
                distancias = list(map(float, fila[1:]))  # Convertir las distancias a float
                gestos.append((nombre_gesto, distancias))
        return gestos


    def comparar_gesto(self, distancias_detectadas, gestos_guardados, umbral=0.5):
        """
        Compara el gesto detectado con los gestos guardados y devuelve el nombre del gesto más cercano.
        """
        gesto_reconocido = None
        menor_diferencia = float('inf')  # Inicializar con infinito

        for nombre_gesto, distancias_gesto_guardado in gestos_guardados:
            try:
                diferencia = np.linalg.norm(np.array(distancias_detectadas) - np.array(distancias_gesto_guardado))
                print(f"Diferencia con {nombre_gesto}: {diferencia}")

                # Si la diferencia es menor al umbral y también la menor hasta ahora
                if diferencia < umbral and diferencia < menor_diferencia:
                    menor_diferencia = diferencia
                    gesto_reconocido = nombre_gesto
            except Exception as e:
                print(f"Error al calcular la diferencia con el gesto '{nombre_gesto}': {e}")

        return gesto_reconocido  # Devuelve el nombre del gesto más cercano o None si no se encontró


