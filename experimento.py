#!/usr/bin/env python3
from mininet.net import Mininet
from mininet.node import Controller, OVSController
from mininet.link import TCLink
from mininet.topo import Topo
import os
import time
import sys

class BufferbloatTopo(Topo):
    def build(self):
        h1, h2 = self.addHost('h1'), self.addHost('h2')
        # SOLUÇÃO: Trocar addHost por addSwitch. 
        # Isso resolve 100% da conectividade L2 e permite o tc-netem funcionar.
        r1 = self.addSwitch('r1') 
        self.addLink(h1, r1, bw=1000, linkopts={'params':{'r2q':1}}) 
        self.addLink(r1, h2, bw=10, delay='20ms')

def rodar():
    buffers, cargas, rep = [10, 100, 500, 1000], [0, 1, 5, 10], 30
    total = len(buffers) * len(cargas) * rep
    cont = 0

    print(f"\n🚀 MARATONA REINICIADA: Conectividade L2 Ativada\n")

    for b in buffers:
        for c in cargas:
            pasta = f"resultados/buffer_{b}_carga_{c}"
            if not os.path.exists(pasta): os.makedirs(pasta)
            
            for r in range(1, rep + 1):
                cont += 1
                
                # Limpeza extrema antes de cada rodada
                os.system("mn -c > /dev/null 2>&1")
                os.system("killall -9 iperf3 ping > /dev/null 2>&1")
                
                net = Mininet(topo=BufferbloatTopo(), link=TCLink, controller=OVSController)
                net.start()
                
                h1, h2, r1 = net.get('h1', 'h2', 'r1')
                
                # Aplica o limite da fila na interface de saída do Switch
                r1.cmd(f"ifconfig r1-eth2 txqueuelen {b}")
                
                print(f"Execução [{cont}/{total}] | B:{b} C:{c} | Rep:{r}...", end='\r')
                sys.stdout.flush()

                # Inicia os servidores
                h2.cmd("iperf3 -s -p 5201 -D")
                h2.cmd("iperf3 -s -p 5202 -D")
                
                # Inicia Ping e Jitter em Background
                h1.cmd(f"ping -c 60 10.0.0.2 > {pasta}/rep_{r}_ping.txt &")
                h1.cmd(f"iperf3 -c 10.0.0.2 -u -b 100k -t 60 -p 5202 -J > {pasta}/rep_{r}_jitter.json &")
                
                # Dispara a Carga (bloqueia o script pelos 60 segundos reais)
                if c > 0:
                    h1.cmd(f"iperf3 -c 10.0.0.2 -t 60 -P {c} -O 10 -p 5201 -J > {pasta}/rep_{r}_tcp.json")
                else:
                    time.sleep(62)
                
                net.stop()
        print(f"\n Buffer {b} concluído.")

    print(f"\n EXPERIMENTO FINALIZADO!")

if __name__ == '__main__':
    rodar()
