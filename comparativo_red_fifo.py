#!/usr/bin/env python3
import json, os, numpy as np, scipy.stats as st, matplotlib.pyplot as plt

buffers = [10, 100, 500, 1000]
rep = 30
carga = 10 #Focar no cenário de estresse máximo!

def obter_stats(pasta, metrica='rtt'):
    valores = []
    for r in range(1, rep + 1):
        try:
            if metrica == 'rtt':
                with open(f"{pasta}/rep_{r}_ping.txt") as f:
                    linha = [l for l in f if "rtt" in l][0]
                    valores.append(float(linha.split("=")[1].split("/")[1]))
            else:
                with open(f"{pasta}/rep_{r}_jitter.json") as f:
                    valores.append(json.load(f)['end']['sum']['jitter_ms'])
        except: pass
    if not valores: return 0, 0
    media = np.mean(valores)
    erro = st.sem(valores) * st.t.ppf((1 + 0.95) / 2., len(valores)-1) if len(valores)>1 else 0
    return media, erro

print("Processando o confronto final: FIFO vs RED...")

fifo_rtt, fifo_err_r, red_rtt, red_err_r = [], [], [], []
fifo_jit, fifo_err_j, red_jit, red_err_j = [], [], [], []

for b in buffers:
    # RTT
    m_f, e_f = obter_stats(f"resultados/buffer_{b}_carga_{carga}", 'rtt')
    m_r, e_r = obter_stats(f"resultados_red/buffer_{b}_carga_{carga}", 'rtt')
    fifo_rtt.append(m_f); fifo_err_r.append(e_f)
    red_rtt.append(m_r); red_err_r.append(e_r)
    
    # JITTER
    m_fj, e_fj = obter_stats(f"resultados/buffer_{b}_carga_{carga}", 'jitter')
    m_rj, e_rj = obter_stats(f"resultados_red/buffer_{b}_carga_{carga}", 'jitter')
    fifo_jit.append(m_fj); fifo_err_j.append(e_fj)
    red_jit.append(m_rj); red_err_j.append(e_rj)

# ----------------- GRÁFICO 1: RTT (FIFO vs RED) -----------------
x = np.arange(len(buffers))
largura = 0.35

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(x - largura/2, fifo_rtt, largura, yerr=fifo_err_r, label='FIFO (Drop-Tail)', color='#cc0000', capsize=5, edgecolor='black', alpha=0.9)
ax.bar(x + largura/2, red_rtt, largura, yerr=red_err_r, label='RED (Inteligente)', color='#11caa0', capsize=5, edgecolor='black', alpha=0.9)

ax.set_title('Confronto de Latência sob Estresse Máximo (10 Fluxos TCP)', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Tamanho do Buffer (Pacotes)', fontsize=12)
ax.set_ylabel('RTT Médio (ms)', fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(buffers, fontsize=11)
ax.legend(fontsize=11)
ax.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('slide_confronto_rtt.png', dpi=300)
plt.close()

# ----------------- GRÁFICO 2: JITTER (FIFO vs RED) -----------------
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(x - largura/2, fifo_jit, largura, yerr=fifo_err_j, label='FIFO (Drop-Tail)', color='#cc0000', capsize=5, edgecolor='black', alpha=0.9)
ax.bar(x + largura/2, red_jit, largura, yerr=red_err_j, label='RED (Inteligente)', color='#11caa0', capsize=5, edgecolor='black', alpha=0.9)

ax.set_title('Confronto de Jitter sob Estresse Máximo (10 Fluxos TCP)', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Tamanho do Buffer (Pacotes)', fontsize=12)
ax.set_ylabel('Jitter Médio (ms)', fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(buffers, fontsize=11)
ax.legend(fontsize=11)
ax.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('slide_confronto_jitter.png', dpi=300)
plt.close()

print("SUCESSO! As imagens do confronto final foram geradas!")
