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
    erro = st.sem(dados) * st.t.ppf((1 + 0.95) / 2., len(dados)-1) if len(dados) > 1 else 0
    return media, erro

dados_rtt = {b: [] for b in buffers}
erros_rtt = {b: [] for b in buffers}
dados_jit = {b: [] for b in buffers}
erros_jit = {b: [] for b in buffers}

print("Lendo os dados brutos e desenhando os Gráficos de Barras...")

for b in buffers:
    for c in cargas:
        rtts, jits = [], []
        pasta = f"resultados/buffer_{b}_carga_{c}"
        for r in range(1, rep + 1):
            try:
                with open(f"{pasta}/rep_{r}_ping.txt") as f:
                    linha = [l for l in f if "rtt" in l][0]
                    rtts.append(float(linha.split("=")[1].split("/")[1]))
                with open(f"{pasta}/rep_{r}_jitter.json") as f:
                    jits.append(json.load(f)['end']['sum']['jitter_ms'])
            except: continue
        
        m_r, e_r = calcular_stats(rtts)
        m_j, e_j = calcular_stats(jits)
        
        dados_rtt[b].append(m_r)
        erros_rtt[b].append(e_r)
        dados_jit[b].append(m_j)
        erros_jit[b].append(e_j)

# Configurações das Barras
largura = 0.2
x = np.arange(len(cargas))  # Posições: [0, 1, 2, 3]
offsets = [-1.5 * largura, -0.5 * largura, 0.5 * largura, 1.5 * largura]
cores = {10: '#11caa0', 100: '#003366', 500: '#ff9900', 1000: '#cc0000'}

# ----------------- GRÁFICO 1: RTT (BARRAS) -----------------
plt.figure(figsize=(12, 7))

for i, b in enumerate(buffers):
    posicoes = x + offsets[i]
    plt.bar(posicoes, dados_rtt[b], width=largura, yerr=erros_rtt[b], 
            label=f'Buffer {b}', color=cores[b], capsize=5, edgecolor='black', alpha=0.9)

plt.title('Impacto da Carga e Tamanho do Buffer no RTT (Latência)', fontsize=15, fontweight='bold', pad=15)
plt.xlabel('Carga (Nº de Fluxos TCP Concorrentes)', fontsize=13)
plt.ylabel('RTT Médio (ms)', fontsize=13)
plt.xticks(x, cargas, fontsize=12)
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.legend(title="Tam. do Buffer", fontsize=11)
plt.tight_layout()
plt.savefig('slide_barras_rtt.png', dpi=300)
plt.close()

# ----------------- GRÁFICO 2: JITTER (BARRAS) -----------------
plt.figure(figsize=(12, 7))

for i, b in enumerate(buffers):
    posicoes = x + offsets[i]
    plt.bar(posicoes, dados_jit[b], width=largura, yerr=erros_jit[b], 
            label=f'Buffer {b}', color=cores[b], capsize=5, edgecolor='black', alpha=0.9)

plt.title('Variação do Atraso (Jitter) sob Congestionamento', fontsize=15, fontweight='bold', pad=15)
plt.xlabel('Carga (Nº de Fluxos TCP Concorrentes)', fontsize=13)
plt.ylabel('Jitter Médio (ms)', fontsize=13)
plt.xticks(x, cargas, fontsize=12)
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.legend(title="Tam. do Buffer", fontsize=11)
plt.tight_layout()
plt.savefig('slide_barras_jitter.png', dpi=300)
plt.close()

print("SUCESSO! As imagens 'slide_barras_rtt.png' e 'slide_barras_jitter.png' foram criadas!")
