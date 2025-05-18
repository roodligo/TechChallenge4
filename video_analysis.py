
import cv2
from deepface import DeepFace
import os
import uuid
from activity_detection import detectar_atividade

def process_video(video_path, output_path):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    emotions_summary = {}
    atividades_summary = {}
    anomalias_detectadas = 0
    saved_faces = {}

    os.makedirs("faces", exist_ok=True)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        # Processar apenas 1 a cada 3 frames
        if frame_count % 3 != 0:
            continue

        atividade, movimento_brusco = detectar_atividade(frame)
        if atividade:
            atividades_summary[atividade] = atividades_summary.get(atividade, 0) + 1
        if movimento_brusco:
            anomalias_detectadas += 1

        try:
            results = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False, detector_backend='mediapipe')
            for result in results:
                emotion = result['dominant_emotion']
                emotions_summary[emotion] = emotions_summary.get(emotion, 0) + 1

                region = result['region']
                x, y, w, h = region['x'], region['y'], region['w'], region['h']

                h_frame, w_frame = frame.shape[:2]
                # Verifica se a região é válida
                if x < 0 or y < 0 or x + w > w_frame or y + h > h_frame:
                    continue

                face = frame[y:y+h, x:x+w]

                saved_faces.setdefault(emotion, [])
                if len(saved_faces[emotion]) < 3:
                    filename = f"faces/{uuid.uuid4().hex}_{emotion}.jpg"
                    cv2.imwrite(filename, face)
                    saved_faces[emotion].append(filename)
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
    import uuid
    from activity_detection import detectar_atividade

    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    emotions_summary = {}
    atividades_summary = {}
    anomalias_detectadas = 0
    saved_faces = {}

    os.makedirs("faces", exist_ok=True)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        # Processar apenas 1 a cada 3 frames
        if frame_count % 3 != 0:
            continue

        atividade, movimento_brusco = detectar_atividade(frame)
        if atividade:
            atividades_summary[atividade] = atividades_summary.get(atividade, 0) + 1
        if movimento_brusco:
            anomalias_detectadas += 1

        try:
            results = DeepFace.analyze(frame, actions=["emotion"], enforce_detection=False, detector_backend='mediapipe')
            for result in results:
                emotion = result['dominant_emotion']
                emotions_summary[emotion] = emotions_summary.get(emotion, 0) + 1

                region = result['region']
                x, y, w, h = region['x'], region['y'], region['w'], region['h']

                h_frame, w_frame = frame.shape[:2]
                if x < 0 or y < 0 or x + w > w_frame or y + h > h_frame:
                    continue

                face = frame[y:y+h, x:x+w]

                saved_faces.setdefault(emotion, [])
                if len(saved_faces[emotion]) < 3:
                    filename = f"faces/{uuid.uuid4().hex}_{emotion}.jpg"
                    cv2.imwrite(filename, face)
                    saved_faces[emotion].append(filename)
        except:
            continue

    cap.release()

    return {
        "total_frames": frame_count,
        "emoções": emotions_summary,
        "atividades": atividades_summary,
        "anomalias": anomalias_detectadas,
        "rostos": saved_faces
    }
