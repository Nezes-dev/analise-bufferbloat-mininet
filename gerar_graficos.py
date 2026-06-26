#!/usr/bin/env python3
import json
import numpy as np
import scipy.stats as st
import os
import matplotlib.pyplot as plt

buffers = [10, 100, 500, 1000]
cargas = [0, 1, 5, 10]
rep = 30

def calcular_stats(dados):
    if not dados: return 0, 0
    media = np.mean(dados)
    # Calcula a margem de erro (IC 95%)
    erro = st.sem(dados) * st.t.ppf((1 + 0.95) / 2., len(dados)-1) if len(dados) > 1 else 0
    return media, erro

# Dicionários para organizar as linhas do gráfico
dados_rtt = {b: [] for b in buffers}
erros_rtt = {b: [] for b in buffers}
dados_jit = {b: [] for b in buffers}
erros_jit = {b: [] for b in buffers}

print("Lendo os dados brutos e desenhando os gráficos...")

for b in buffers:
    for c in cargas:
        rtts, jits = [], []
        pasta = f"resultados/buffer_{b}_carga_{c}"
        for r in range(1, rep + 1):
            try:
                # Coleta RTT
                with open(f"{pasta}/rep_{r}_ping.txt") as f:
                    linha = [l for l in f if "rtt" in l][0]
                    rtts.append(float(linha.split("=")[1].split("/")[1]))
                # Coleta Jitter
                with open(f"{pasta}/rep_{r}_jitter.json") as f:
                    jits.append(json.load(f)['end']['sum']['jitter_ms'])
            except: continue
        
        m_r, e_r = calcular_stats(rtts)
        m_j, e_j = calcular_stats(jits)
        
        dados_rtt[b].append(m_r)
        erros_rtt[b].append(e_r)
        dados_jit[b].append(m_j)
        erros_jit[b].append(e_j)

# ----------------- GRÁFICO 1: RTT (LATÊNCIA) -----------------
plt.figure(figsize=(10, 6))
marcadores = {10: 'o', 100: 's', 500: '^', 1000: 'D'}
cores = {10: '#11caa0', 100: '#003366', 500: '#ff9900', 1000: '#cc0000'}

for b in buffers:
    plt.errorbar(cargas, dados_rtt[b], yerr=erros_rtt[b], label=f'Buffer {b}', 
                 marker=marcadores[b], color=cores[b], capsize=5, linewidth=2, markersize=8)

plt.title('Impacto da Carga TCP e Tamanho do Buffer no RTT (Latência)', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Carga (Nº de Fluxos TCP Concorrentes)', fontsize=12)
plt.ylabel('RTT Médio (ms)', fontsize=12)
plt.xticks(cargas)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(title="Tam. do Buffer", fontsize=10)
plt.tight_layout()
plt.savefig('slide_grafico_rtt.png', dpi=300)
plt.close()

# ----------------- GRÁFICO 2: JITTER -----------------
plt.figure(figsize=(10, 6))

for b in buffers:
    plt.errorbar(cargas, dados_jit[b], yerr=erros_jit[b], label=f'Buffer {b}', 
                 marker=marcadores[b], color=cores[b], capsize=5, linewidth=2, markersize=8)

plt.title('Variação do Atraso (Jitter) sob Congestionamento', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Carga (Nº de Fluxos TCP Concorrentes)', fontsize=12)
plt.ylabel('Jitter Médio (ms)', fontsize=12)
plt.xticks(cargas)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(title="Tam. do Buffer", fontsize=10)
plt.tight_layout()
plt.savefig('slide_grafico_jitter.png', dpi=300)
plt.close()

print("SUCESSO! As imagens 'slide_grafico_rtt.png' e 'slide_grafico_jitter.png' foram criadas na pasta atual.")
