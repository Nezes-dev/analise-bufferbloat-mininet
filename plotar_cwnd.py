#!/usr/bin/env python3
import json
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt

# Parâmetros Estratégicos
buffer_alvo = 1000
carga_alvo = 1 
reps = 30
tempos = np.arange(1, 61) 

def extrair_cwnd(pasta):
    cwnd_matriz = []
    for r in range(1, reps + 1):
        try:
            with open(f"{pasta}/rep_{r}_tcp.json") as f:
                dados = json.load(f)
                cwnd_run = []
                
                for intervalo in dados.get('intervals', []):
                    try:
                        # Extrai a janela em KiloBytes
                        cwnd_bytes = intervalo['streams'][0]['snd_cwnd']
                        cwnd_run.append(cwnd_bytes / 1024)
                    except KeyError:
                        continue
                
                # Se o iperf3 registrou 70 seg (por causa do -O 10), pegamos os últimos 60
                if len(cwnd_run) >= 60:
                    cwnd_matriz.append(cwnd_run[-60:])
        except Exception as e:
            continue
            
    if not cwnd_matriz:
        print(f"⚠️ Atenção: Nenhum dado válido encontrado na pasta {pasta}.")
        return np.zeros(60), np.zeros(60)
        
    cwnd_matriz = np.array(cwnd_matriz)
    medias = np.mean(cwnd_matriz, axis=0)
    
    erros = []
    for sec in range(60):
        dados_segundo = cwnd_matriz[:, sec]
        if len(dados_segundo) > 1:
            erro = st.sem(dados_segundo) * st.t.ppf((1 + 0.95) / 2., len(dados_segundo)-1)
        else:
            erro = 0
        erros.append(erro)
        
    return medias, np.array(erros)

print("🔍 Processando Janelas TCP (cwnd) da Fila FIFO...")
m_fifo, e_fifo = extrair_cwnd(f"resultados/buffer_{buffer_alvo}_carga_{carga_alvo}")

print("🔍 Processando Janelas TCP (cwnd) da Fila RED...")
m_red, e_red = extrair_cwnd(f"resultados_red/buffer_{buffer_alvo}_carga_{carga_alvo}")

plt.figure(figsize=(12, 6))

plt.plot(tempos, m_fifo, label='FIFO (Drop-Tail)', color='#d62728', linewidth=2.5)
plt.fill_between(tempos, m_fifo - e_fifo, m_fifo + e_fifo, color='#d62728', alpha=0.2)

plt.plot(tempos, m_red, label='RED (Active Queue Management)', color='#2ca02c', linewidth=2.5)
plt.fill_between(tempos, m_red - e_red, m_red + e_red, color='#2ca02c', alpha=0.2)

plt.title(f"Dinâmica da Janela de Congestionamento TCP (cwnd)\nBuffer: {buffer_alvo} pacotes | Carga: {carga_alvo} Fluxo TCP Concorrente", fontsize=14, fontweight='bold')
plt.xlabel("Tempo de Simulação (Segundos)", fontsize=12)
plt.ylabel("Tamanho Médio da Janela - cwnd (KB)", fontsize=12)
plt.legend(loc="upper left", fontsize=11, framealpha=0.9)
plt.grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
nome_arquivo = "grafico_cwnd_corrigido.png"
plt.savefig(nome_arquivo, dpi=300)

print(f"✅ SUCESSO! Gráfico salvo como '{nome_arquivo}'.")
