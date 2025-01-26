import numpy as np


class Normalizar:
    def __init__(self):
        pass
    
    def normalizar_landmarks(landmarks):
        """Normaliza los landmarks para que sean relativos a la base de la palma."""
        base_x, base_y, base_z = landmarks[0]
        landmarks_normalizados = []
        for x, y, z in landmarks:
            landmarks_normalizados.append((x - base_x, y - base_y, z - base_z))
        return landmarks_normalizados

    def escalar_landmarks(landmarks):
        """Escala los landmarks para que estén dentro de un rango uniforme."""
        max_val = max(max(abs(x), abs(y), abs(z)) for x, y, z in landmarks)
        landmarks_escalados = [(x / max_val, y / max_val, z / max_val) for x, y, z in landmarks]
        return landmarks_escalados


    def calcular_distancias(landmarks):
        """Calcula las distancias entre cada par de landmarks."""
        distancias = []
        for i in range(len(landmarks)):
            for j in range(i + 1, len(landmarks)):
                distancias.append(np.linalg.norm(np.array(landmarks[i]) - np.array(landmarks[j])))
        return distancias
