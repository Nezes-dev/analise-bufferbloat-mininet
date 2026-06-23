#!/usr/bin/env python3
import json
import numpy as np
import scipy.stats as st
from scipy import stats
import os

buffers, cargas, rep = [10, 100, 500, 1000], [0, 1, 5, 10], 30

def calcular(dados):
    if not dados or len(dados) < 2: return 0.0, 0.0, 0.0
    media = np.mean(dados)
    margem = st.sem(dados) * st.t.ppf((1 + 0.95) / 2., len(dados)-1)
    moda = stats.mode(np.round(dados, 1), keepdims=True).mode[0]
    return media, moda, margem

print(f"{'CENÁRIO':<15} | {'RTT (ms) ± IC':<18} | {'JITTER (ms) ± IC':<18}")
print("-" * 60)

for b in buffers:
    for c in cargas:
        r_list, j_list = [], []
        p = f"resultados/buffer_{b}_carga_{c}"
        for r in range(1, rep + 1):
            try:
                with open(f"{p}/rep_{r}_ping.txt") as f:
                    v = [l for l in f if "rtt" in l][0].split("=")[1].split("/")[1]
                    r_list.append(float(v))
                with open(f"{p}/rep_{r}_jitter.json") as f:
                    j_list.append(json.load(f)['end']['sum']['jitter_ms'])
            except: continue
        
        m_r, mo_r, ic_r = calcular(r_list)
        m_j, mo_j, ic_j = calcular(j_list)
        print(f"B:{b:<4} C:{c:<2} | {m_r:>5.1f} ± {ic_r:>4.2f} | {m_j:>6.2f} ± {ic_j:>4.2f}")
