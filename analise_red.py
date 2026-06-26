#!/usr/bin/env python3
import json
import numpy as np
import scipy.stats as st

buffers = [10, 100, 500, 1000]
cargas = [0, 1, 5, 10]
rep = 30

def calcular_stats(dados):
    if not dados: return 0.0, 0.0
    media = np.mean(dados)
    erro = st.sem(dados) * st.t.ppf((1 + 0.95) / 2., len(dados)-1) if len(dados) > 1 else 0
    return round(media, 1), round(erro, 2)

print(f"{'CENÁRIO':<15} | {'RTT (ms) ± IC':<18} | {'JITTER (ms) ± IC'}")
print("-" * 60)

for b in buffers:
    for c in cargas:
        rtts, jits = [], []
        pasta = f"resultados_red/buffer_{b}_carga_{c}"
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
        print(f"B:{b:<4} C:{c:<2} | {m_r:>7} ± {e_r:<6} | {m_j:>7} ± {e_j:<6}")
