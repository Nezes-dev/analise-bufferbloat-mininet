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
  <em>Análise quantitativa do impacto do tamanho de filas na latência e vazão TCP, comparando políticas FIFO (Drop-Tail) e RED (Active Queue Management). Projeto acadêmico para a disciplina de Analise de Desempenho de Redes de Computadores - UFC Quixadá.</em>
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
 ┗ 📂 resultados/                  # Arquivos .txt, .json e .csv gerados pelas 960 execuções

```

---

## ⚙️ Metodologia Estatística

O experimento foi desenhado com rigor para evitar anomalias de emulação:

* **Fatores:** Tamanho do Buffer (10, 100, 500, 1000 pacotes) vs Carga (0, 1, 5, 10 fluxos TCP).
* **Execuções:** 30 rodadas independentes de 60 segundos por cenário (total de 480 emulações por fila, 960 no total geral).
* **Confiabilidade:** Margem de erro calculada utilizando **Intervalo de Confiança (IC) de 95%** com distribuição T-Student.

---

## 🚀 Como Executar

### Pré-requisitos

Certifique-se de estar rodando um ambiente Linux (Ubuntu recomendado) e instale as dependências:

```bash
sudo apt update
sudo apt install mininet iperf3 -y
pip install matplotlib numpy scipy

```

### 1. Iniciar a Emulação

Para rodar os testes da fila tradicional (FIFO):

```bash
sudo python3 experimento.py

```

Para rodar os testes com o gerenciamento ativo (RED):

```bash
sudo python3 experimento_red.py

```

### 2. Processar os Dados

```bash
python3 analise.py
python3 gerar_graficos.py

```

---

## 📈 Resultados em Destaque

### O Confronto: FIFO vs RED (Carga Extrema)

Sob estresse máximo (10 fluxos TCP contra um buffer de 1000 pacotes), a fila FIFO retém pacotes causando uma latência destrutiva, enquanto o RED descarta preventivamente e educa o TCP.

| Métrica | FIFO (Drop-Tail) 🟥 | RED (Inteligente) 🟩 | Melhoria |
| --- | --- | --- | --- |
| **Latência (RTT)** | `4354.1 ± 1171.83 ms` | `38.7 ± 4.56 ms` | **112.4x** |
| **Jitter** | `123.20 ± 38.93 ms` | `9.6 ± 3.96 ms` | **12.8x** |
| **Retransmissões** | `1236 pacotes` | `45 pacotes` | **-96% perdas** |

*(Para ver os gráficos gerados com o detalhamento das barras de erro e a dinâmica da janela TCP, consulte as imagens e o relatório em PDF disponibilizados nos arquivos do repositório).*

---

## 🏁 Conclusão

A emulação prova que a adição cega de memória em roteadores causa degradação extrema da rede moderna. A parametrização de algoritmos de Active Queue Management (AQM), como o RED, é indispensável para preservar o Quality of Service (QoS) em aplicações sensíveis ao tempo (VoIP, Jogos, Vídeo).
