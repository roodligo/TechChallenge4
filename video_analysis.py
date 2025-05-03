import cv2
from deepface import DeepFace
import os
from activity_detection import detectar_atividade

def process_video(video_path, output_path):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    emotions_summary = {}
    atividades_summary = {}
    anomalias_detectadas = 0  # Inicializa a contagem de anomalias

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        # Detecção de atividade
        atividade, movimento_brusco = detectar_atividade(frame)

        if atividade:
            atividades_summary[atividade] = atividades_summary.get(atividade, 0) + 1

        if movimento_brusco:
            anomalias_detectadas += 1

        # Detecção de emoções
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = frame[y:y+h, x:x+w]
            try:
                result = DeepFace.analyze(face, actions=["emotion"], enforce_detection=False, detector_backend='opencv')
                emotion = result[0]['dominant_emotion']
                emotions_summary[emotion] = emotions_summary.get(emotion, 0) + 1
            except:
                continue

    cap.release()

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"Total de frames analisados: {frame_count}\n\n")

        f.write("Resumo das emoções detectadas:\n")
        for emotion, count in emotions_summary.items():
            f.write(f"  {emotion}: {count} vezes\n")

        f.write("\nResumo das atividades detectadas:\n")
        for atividade, count in atividades_summary.items():
            f.write(f"  {atividade}: {count} vezes\n")

        f.write(f"\nTotal de anomalias detectadas: {anomalias_detectadas}\n")


def process_video_return_data(video_path):
    import cv2
    from deepface import DeepFace
    from activity_detection import detectar_atividade

    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    emotions_summary = {}
    atividades_summary = {}
    anomalias_detectadas = 0

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        atividade, movimento_brusco = detectar_atividade(frame)

        if atividade:
            atividades_summary[atividade] = atividades_summary.get(atividade, 0) + 1

        if movimento_brusco:
            anomalias_detectadas += 1

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = frame[y:y+h, x:x+w]
            try:
                result = DeepFace.analyze(face, actions=["emotion"], enforce_detection=False, detector_backend='opencv')
                emotion = result[0]['dominant_emotion']
                emotions_summary[emotion] = emotions_summary.get(emotion, 0) + 1
            except:
                continue

    cap.release()

    return {
        "total_frames": frame_count,
        "emoções": emotions_summary,
        "atividades": atividades_summary,
        "anomalias": anomalias_detectadas
    }
