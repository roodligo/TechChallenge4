# Analisador de Emoções, Atividades e Anomalias em Vídeo

## Objetivo

Este projeto realiza a análise automática de vídeos para:

- Detecção de rostos e expressões faciais
- Análise de emoções com DeepFace
- Detecção de atividades com MediaPipe (em pé, sentado, levantando braço)
- Identificação de anomalias com base em movimentos bruscos
- Geração de gráficos interativos e relatório final em PDF

---

## Tecnologias Utilizadas

- Python 3.10
- Streamlit (interface web)
- OpenCV
- DeepFace
- MediaPipe
- Matplotlib
- FPDF (geração de PDF)

---

## Instalação

1. Clone o projeto:

2. Crie o ambiente virtual:

```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/macOS
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## Executando o sistema

Com o ambiente virtual ativado, execute:

```bash
streamlit run streamlit_app.py
```

1. Faça o upload do vídeo no formato `.mp4`, `.avi` ou `.mov`
2. Clique em "Analisar"
3. Visualize os gráficos gerados
4. Clique em "Baixar relatório em PDF" para gerar o arquivo com o resumo e os gráficos

---

## Estrutura do Projeto

```
.
├── activity_detection.py         # Detecção de atividades e anomalias
├── report_generator.py          # Geração do relatório PDF com gráficos
├── streamlit_app.py             # Interface com Streamlit
├── video_analysis.py            # Processamento de vídeo e análise
├── requirements.txt             # Dependências do projeto
```

---

## Exemplo de saída no PDF

- Total de frames analisados
- Contagem de cada emoção
- Contagem de cada atividade
- Total de anomalias detectadas
- Gráfico de barras (emoções)
- Gráfico de pizza (atividades)

---

## Observações

- A precisão depende da qualidade do vídeo e iluminação.
- O sistema identifica anomalias com base na variação de movimento corporal entre frames.
