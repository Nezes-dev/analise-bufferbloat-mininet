#!/usr/bin/env python3
from mininet.net import Mininet
from mininet.node import OVSController
from mininet.link import TCLink
from mininet.topo import Topo
import os
import time
import sys

class BufferbloatTopo(Topo):
    def build(self):
        h1, h2 = self.addHost('h1'), self.addHost('h2')
        r1 = self.addSwitch('r1') 
        self.addLink(h1, r1, bw=1000, linkopts={'params':{'r2q':1}}) 
        self.addLink(r1, h2, bw=10, delay='20ms')

def rodar():
    buffers = [10, 100, 500, 1000]
    cargas = [0, 1, 5, 10]
    rep = 30
    total = len(buffers) * len(cargas) * rep
    cont = 0

    print(f"\n MARATONA RED INICIADA: Fila Inteligente Ativada\n")

    for b in buffers:
        for c in cargas:
            # NOVA PASTA: Para não misturar com os dados da fila FIFO
            pasta = f"resultados_red/buffer_{b}_carga_{c}"
            if not os.path.exists(pasta): os.makedirs(pasta)
            
            for r in range(1, rep + 1):
                cont += 1
                
                os.system("mn -c > /dev/null 2>&1")
                os.system("killall -9 iperf3 ping > /dev/null 2>&1")
                
                net = Mininet(topo=BufferbloatTopo(), link=TCLink, controller=OVSController)
                net.start()
                
                h1, h2, r1 = net.get('h1', 'h2', 'r1')
                
                # --- MÁGICA DA FILA RED ---
                # Limpa qualquer regra de fila anterior
                r1.cmd("tc qdisc del dev r1-eth2 root 2> /dev/null")
                
                # O RED calcula limites em Bytes (1 pacote = ~1500 bytes no MTU padrão)
                limite_bytes = b * 1500
                min_bytes = int(limite_bytes * 0.25) # Começa a descartar com 25% da fila cheia
                max_bytes = int(limite_bytes * 0.75) # Descarta agressivamente com 75%
                
                # Aplica a regra RED nativa do Linux no Switch
                comando_red = f"tc qdisc add dev r1-eth2 root red limit {limite_bytes} min {min_bytes} max {max_bytes} avpkt 1500 burst 20 probability 0.1 ecn"
                r1.cmd(comando_red)
                # --------------------------
                
                print(f"Execução RED [{cont}/{total}] | B:{b} C:{c} | Rep:{r}...", end='\r')
                sys.stdout.flush()

                h2.cmd("iperf3 -s -p 5201 -D")
                h2.cmd("iperf3 -s -p 5202 -D")
                
                h1.cmd(f"ping -c 60 10.0.0.2 > {pasta}/rep_{r}_ping.txt &")
                h1.cmd(f"iperf3 -c 10.0.0.2 -u -b 100k -t 60 -p 5202 -J > {pasta}/rep_{r}_jitter.json &")
                
                if c > 0:
                    h1.cmd(f"iperf3 -c 10.0.0.2 -t 60 -P {c} -O 10 -p 5201 -J > {pasta}/rep_{r}_tcp.json")
                else:
                    time.sleep(62)
                
                net.stop()
        print(f"\n Buffer RED {b} concluído.")

    print(f"\n EXPERIMENTO RED FINALIZADO!")

if __name__ == '__main__':
    rodar()
