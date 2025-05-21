
from fpdf import FPDF
import matplotlib.pyplot as plt

def gerar_relatorio_pdf(data, filename="relatorio.pdf"):
    # Gerar gráfico de emoções
    plt.figure(figsize=(6, 4))
    plt.bar(data["emoções"].keys(), data["emoções"].values())
    plt.title("Distribuição de Emoções")
    plt.ylabel("Ocorrências")
    plt.tight_layout()
    plt.savefig("grafico_emocoes.png")
    plt.close()

    # Gerar gráfico de atividades
    plt.figure(figsize=(6, 4))
    plt.pie(data["atividades"].values(), labels=data["atividades"].keys(), autopct="%1.1f%%", startangle=140)
    plt.title("Distribuição de Atividades")
    plt.axis("equal")
    plt.tight_layout()
    plt.savefig("grafico_atividades.png")
    plt.close()

    # Criar o PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Relatório de Análise de Vídeo", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Total de frames analisados: {data['total_frames']}", ln=True)
    pdf.cell(0, 10, f"Total de anomalias detectadas: {data['anomalias']}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Resumo das Emoções:", ln=True)
    pdf.set_font("Arial", "", 12)
    for emo, count in data["emoções"].items():
        pdf.cell(0, 10, f"  {emo}: {count} vezes", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Resumo das Atividades:", ln=True)
    pdf.set_font("Arial", "", 12)
    for act, count in data["atividades"].items():
        pdf.cell(0, 10, f"  {act}: {count} vezes", ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Gráficos:", ln=True)
    pdf.ln(5)

    pdf.image("grafico_emocoes.png", w=170)
    pdf.ln(5)
    pdf.image("grafico_atividades.png", w=170)

    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Exemplos de rostos detectados:", ln=True)
    pdf.ln(5)

    for emo, paths in data.get("rostos", {}).items():
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, f"{emo}:", ln=True)
        for i, path in enumerate(paths):
            try:
                pdf.image(path, w=50)
            except:
                pdf.set_font("Arial", "", 12)
                pdf.cell(0, 10, f"(erro ao carregar imagem {i+1})", ln=True)
        pdf.ln(5)

    pdf.output(filename)
