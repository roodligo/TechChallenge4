import mediapipe as mp
import cv2
import math

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False)
previous_landmarks = None  # Mantém a pose anterior


def calcular_distancia(p1, p2):
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


def detectar_atividade(frame):
    global previous_landmarks
    atividade = "desconhecida"
    movimento_brusco = False

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultado = pose.process(rgb)

    if resultado.pose_landmarks:
        pontos = resultado.pose_landmarks.landmark

        # Atividade com base no quadril e joelho
        quadril = pontos[mp_pose.PoseLandmark.LEFT_HIP]
        joelho = pontos[mp_pose.PoseLandmark.LEFT_KNEE]

        if quadril.y < joelho.y:
            atividade = "em pé"
        else:
            atividade = "sentado"

        # Levantando braço
        mao_direita = pontos[mp_pose.PoseLandmark.RIGHT_WRIST]
        ombro_direito = pontos[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        if mao_direita.y < ombro_direito.y:
            atividade = "levantando braço"

        # Cálculo do movimento brusco
        if previous_landmarks:
            deslocamentos = []
            for i in range(len(pontos)):
                deslocamentos.append(calcular_distancia(pontos[i], previous_landmarks[i]))

            media_deslocamento = sum(deslocamentos) / len(deslocamentos)

            if media_deslocamento > 0.05:  # limiar ajustável
                movimento_brusco = True

        previous_landmarks = pontos

    return atividade, movimento_brusco
