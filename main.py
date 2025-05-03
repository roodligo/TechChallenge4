from video_analysis import process_video

if __name__ == "__main__":
    video_path = "assets/Unlocking_Facial_Recognition_Diverse Activities_Analysis.mp4"  # coloque aqui o caminho correto do vídeo
    output_path = "output_summary.txt"
    process_video(video_path, output_path)
