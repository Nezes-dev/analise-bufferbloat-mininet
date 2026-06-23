# 🌐 Análise do Fenômeno Bufferbloat com Mininet

Este repositório contém os scripts de automação, emulação e análise estatística desenvolvidos para quantificar o impacto do tamanho dos buffers na latência e no jitter de redes de computadores, evidenciando o problema do **Bufferbloat**.

## 🎯 Objetivos do Projeto
* Mensurar o impacto prático do tamanho de filas (buffers) no tempo de ida e volta (RTT) e na variação de atraso (Jitter).
* Avaliar o comportamento da rede sob diferentes níveis de estresse (0, 1, 5 e 10 fluxos TCP concorrentes).
* Comparar o desempenho da política de descarte padrão **FIFO (Drop-Tail)** com o algoritmo de gerenciamento ativo de filas **RED (Random Early Detection)**.

## 🛠️ Tecnologias e Ferramentas Utilizadas
* **Emulador:** Mininet (Topologia em árvore/estrela)
* **Controlador:** OVS (Open vSwitch) L2
* **Geradores de Tráfego:** `iperf3` (TCP para estresse, UDP para Jitter) e `ping` (ICMP para RTT)
* **Automação e Análise:** Python 3 (Bibliotecas: `numpy`, `scipy.stats`, `matplotlib`)
* **Sistema Operacional:** Linux (Ubuntu/Debian) com manipulação de tráfego via `tc qdisc`

## 📊 Metodologia
O experimento foi desenhado com rigor estatístico:
1. **Fatores e Níveis:** Tamanhos de Buffer (10, 100, 500, 1000 pacotes) cruzados com Cargas de Tráfego (0, 1, 5, 10 fluxos TCP).
2. **Repetições:** 30 rodadas independentes para cada cenário, com 60 segundos de duração por rodada.
3. **Confiabilidade:** Cálculo de margem de erro utilizando Intervalo de Confiança (IC) de 95% com distribuição T-Student.

## 🚀 Como Executar

```bash
1.Emulação da Fila FIFO (Drop-Tail):
sudo python3 experimento.py

2. Emulação da Fila Inteligente (RED):
sudo python3 experimento_red.py

3. Geração das Estatísticas e Gráficos
python3 analise.py
python3 gerar_graficos.py
python3 comparativo_red_fifo.py



Desenvolvido por Nicollas e Kêmilly.

