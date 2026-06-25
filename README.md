<h1 align="center">
  🌐 Análise do Fenômeno Bufferbloat em Redes Emuladas
</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Autor-Nicollas-1f497d?style=flat-square&logo=github">
  <img src="https://img.shields.io/badge/Co--Autora-Kêmilly-1f497d?style=flat-square&logo=github">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Ubuntu-E95420?style=flat-square&logo=ubuntu&logoColor=white">
  <img src="https://img.shields.io/badge/Mininet-000000?style=flat-square&logo=linux&logoColor=white">
  <img src="https://img.shields.io/badge/Status-Concluído-success?style=flat-square">
</p>

<p align="center">
  <em>Análise quantitativa do impacto do tamanho de filas na latência e vazão TCP, comparando políticas FIFO (Drop-Tail) e RED (Active Queue Management). Projeto acadêmico para a disciplina de Redes de Computadores - UFC Quixadá.</em>
</p>

<hr>

## 📑 Índice
- [Visão Geral](#-visão-geral)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Metodologia Estatística](#-metodologia-estatística)
- [Como Executar](#-como-executar)
- [Resultados em Destaque](#-resultados-em-destaque)
- [Conclusão](#-conclusão)

---

## 🔬 Visão Geral
O **Bufferbloat** é um fenômeno caracterizado por latências e jitter excessivos causados pelo superdimensionamento de buffers em roteadores. Este projeto utiliza o **Mininet** para emular gargalos de rede (10 Mbps / 20ms de atraso) e provar matematicamente como o mecanismo **RED (Random Early Detection)** salva o protocolo TCP do colapso enfrentado pela tradicional fila **FIFO**.

---

## 📁 Estrutura do Projeto

```text
📦 analise-bufferbloat-mininet
 ┣ 📜 experimento.py               # Emulação da fila FIFO (Drop-Tail)
 ┣ 📜 experimento_red.py           # Emulação da fila inteligente (RED)
 ┣ 📜 analise.py                   # Consolidação de RTT e Jitter (Média + IC 95%)
 ┣ 📜 gerar_graficos.py            # Geração dos gráficos de barras (Matplotlib)
 ┣ 📜 comparativo_red_fifo.py      # Script de confronto direto entre as filas
 ┣ 📜 plotar_cwnd.py               # Extração da Dinâmica da Janela TCP
 ┣ 📜 Relatorio_Final.pdf          # Artigo técnico completo com a fundamentação
 ┗ 📂 resultados/                  # Arquivos .txt, .json e .csv gerados pelas 480 execuçõe


