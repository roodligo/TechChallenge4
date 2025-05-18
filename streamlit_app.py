
import streamlit as st
import matplotlib.pyplot as plt
from video_analysis import process_video_return_data
from report_generator import gerar_relatorio_pdf

st.set_page_config(page_title="Análise de Emoções e Atividades", layout="centered")
st.title("Análise de Emoções, Atividades e Anomalias em Vídeo")

video_file = st.file_uploader("Selecione o vídeo", type=["mp4", "avi", "mov"])

# Inicializar estado da sessão
if "data" not in st.session_state:
    st.session_state.data = None
if "video_path" not in st.session_state:
    st.session_state.video_path = None

# Salvar o vídeo enviado
if video_file is not None:
    temp_video_path = f"temp_{video_file.name}"
    with open(temp_video_path, "wb") as f:
        f.write(video_file.read())
    st.session_state.video_path = temp_video_path

# Botão para iniciar a análise
if st.session_state.video_path and st.button("Analisar"):
    with st.spinner("Processando vídeo..."):
        st.session_state.data = process_video_return_data(st.session_state.video_path)
    st.success("Análise concluída!")

# Mostrar resultados, se houver
if st.session_state.data:
    data = st.session_state.data

    st.markdown(f"**Total de frames analisados:** {data['total_frames']}")
    st.markdown(f"**Total de anomalias detectadas:** {data['anomalias']}")

    st.subheader("Emoções detectadas")
    fig1, ax1 = plt.subplots()
    ax1.bar(data["emoções"].keys(), data["emoções"].values())
    ax1.set_ylabel("Ocorrências")
    ax1.set_title("Distribuição de Emoções")
    st.pyplot(fig1)

    st.subheader("Atividades detectadas")
    fig2, ax2 = plt.subplots()
    ax2.pie(data["atividades"].values(), labels=data["atividades"].keys(), autopct="%1.1f%%", startangle=140)
    ax2.axis("equal")
    st.pyplot(fig2)

    st.subheader("Exemplos de rostos detectados")
    for emo, imagens in data["rostos"].items():
        for i, path in enumerate(imagens):
            st.image(path, caption=f"{emo} ({i+1})", width=200)

    gerar_relatorio_pdf(data)
    with open("relatorio.pdf", "rb") as f:
        st.download_button("Baixar relatório em PDF", f, file_name="relatorio.pdf")
