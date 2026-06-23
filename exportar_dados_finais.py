#!/usr/bin/env python3
import json
import numpy as np
import scipy.stats as st
import os
import csv

buffers = [10, 100, 500, 1000]
cargas = [1, 5, 10] # Omitindo Carga 0 pois não tem tráfego TCP/Vazão
rep = 30

def obter_stats_ping_jitter(pasta):
    rtts, jits = [], []
    for r in range(1, rep + 1):
        try:
            with open(f"{pasta}/rep_{r}_ping.txt") as f:
                linha = [l for l in f if "rtt" in l][0]
                rtts.append(float(linha.split("=")[1].split("/")[1]))
            with open(f"{pasta}/rep_{r}_jitter.json") as f:
                jits.append(json.load(f)['end']['sum']['jitter_ms'])
        except: continue
    
    m_r = np.mean(rtts) if rtts else 0
    m_j = np.mean(jits) if jits else 0
    return round(m_r, 2), round(m_j, 2)

def obter_stats_tcp(pasta):
    vazoes, retransmissoes = [], []
    for r in range(1, rep + 1):
        try:
            with open(f"{pasta}/rep_{r}_tcp.json") as f:
                dados = json.load(f)
                vazoes.append(dados['end']['sum_sent']['bits_per_second'] / 1_000_000)
                retransmissoes.append(dados['end']['sum_sent']['retransmits'])
        except: continue
    
    m_v = np.mean(vazoes) if vazoes else 0
    m_rtx = np.mean(retransmissoes) if retransmissoes else 0
    return round(m_v, 2), round(m_rtx, 0)

caminho_csv = 'metricas_completas_finais.csv'
print("Compilando o arquivo definitivo com RTT, Jitter, Vazão e Retransmissões...")

with open(caminho_csv, mode='w', newline='', encoding='utf-8') as arquivo_csv:
    escritor = csv.writer(arquivo_csv, delimiter=';')
    
    # Cabeçalho
    escritor.writerow(['Fila', 'Buffer (Pacotes)', 'Carga (Fluxos TCP)', 'RTT Medio (ms)', 'Jitter Medio (ms)', 'Vazao Media (Mbps)', 'Retransmissoes Totais'])
    
    filas = [('FIFO', 'resultados'), ('RED', 'resultados_red')]
    
    for nome_fila, diretorio in filas:
        for b in buffers:
            for c in cargas:
                pasta = f"{diretorio}/buffer_{b}_carga_{c}"
                rtt, jitter = obter_stats_ping_jitter(pasta)
                vazao, rtx = obter_stats_tcp(pasta)
                
                escritor.writerow([nome_fila, b, c, rtt, jitter, vazao, rtx])

print(f"✅ SUCESSO! Arquivo '{caminho_csv}' gerado. Importe para o Excel!")
