#!/usr/bin/env python3
import json
import numpy as np
import scipy.stats as st
import os
import csv

buffers = [10, 100, 500, 1000]
cargas = [0, 1, 5, 10]
rep = 30

def calcular_stats(dados):
    if not dados: return 0.0, 0.0
    media = np.mean(dados)
    # Calcula a margem de erro (IC 95%)
    erro = st.sem(dados) * st.t.ppf((1 + 0.95) / 2., len(dados)-1) if len(dados) > 1 else 0
    return round(media, 2), round(erro, 2)

caminho_csv = 'dados_experimento.csv'

print("Extraindo os dados para a planilha...")

# Abre o ficheiro CSV para escrita
with open(caminho_csv, mode='w', newline='', encoding='utf-8') as arquivo_csv:
    escritor = csv.writer(arquivo_csv, delimiter=';') # Ponto e vírgula para o Excel PT-BR
    
    # Escreve o Cabeçalho da Planilha
    escritor.writerow(['Buffer (Pacotes)', 'Carga (Fluxos TCP)', 'RTT Medio (ms)', 'Margem Erro RTT (+/-)', 'Jitter Medio (ms)', 'Margem Erro Jitter (+/-)'])
    
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
            
            # Escreve a linha com os dados calculados
            escritor.writerow([b, c, m_r, e_r, m_j, e_j])

print(f"SUCESSO! Planilha '{caminho_csv}' gerada com sucesso e pronta para o Excel/Google Sheets.")
