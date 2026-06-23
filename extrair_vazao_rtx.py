#!/usr/bin/env python3
import json
import numpy as np

buffers = [10, 100, 500, 1000]
cargas = [1, 5, 10] # Carga 0 não tem TCP, então não tem vazão/retransmissão
rep = 30

print(f"{'CENÁRIO':<15} | {'VAZÃO MÉDIA (Mbps)':<20} | {'RETRANSMISSÕES TOTAIS'}")
print("-" * 65)

for b in buffers:
    for c in cargas:
        vazoes = []
        retransmissoes = []
        pasta = f"resultados/buffer_{b}_carga_{c}" # Lendo da fila FIFO
        
        for r in range(1, rep + 1):
            try:
                with open(f"{pasta}/rep_{r}_tcp.json") as f:
                    dados = json.load(f)
                    # Extrai a vazão em Mbps
                    vazao_bps = dados['end']['sum_sent']['bits_per_second']
                    vazoes.append(vazao_bps / 1_000_000) 
                    
                    # Extrai o total de retransmissões
                    retransmissoes.append(dados['end']['sum_sent']['retransmits'])
            except:
                continue
        
        if vazoes and retransmissoes:
            media_vazao = np.mean(vazoes)
            media_rtx = np.mean(retransmissoes)
            print(f"B:{b:<4} C:{c:<2} | {media_vazao:>10.2f} Mbps      | {media_rtx:>10.0f} pacotes perdidos/reenviados")

print("-" * 65)
print("Dica: Note como buffers menores perdem pacotes (Drop-Tail), forçando mais retransmissões!")

