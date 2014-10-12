import scapy.all as scp
import socket
from collections import Counter
ICMP_TTL_EXC = 11

class RouteTracer:

    def __init__(self, dst, times=1, hops=30):
        self.dst    = dst
        self.times  = times
        self.hops   = hops

    def ip_a_alcanzar(self):
        pkt = scp.IP(dst=self.dst) / scp.ICMP()
        ans, _ = scp.sr(pkt, verbose=0)

        return ans[0][0].dst

    def nodo_a_distancia(self, ttl):
        #Devuelve la tupla (ip, rtt prom) del nodo a distancia ttl
    
        apariciones = Counter()
        tiempo = Counter()
 
        dst = self.dst
        pkt = scp.IP(dst=dst, ttl=ttl) / scp.ICMP()  
        dst_ip = pkt.dst

        for i in xrange(self.times):
            ans, unans = scp.sr(pkt, verbose=0, timeout=1)

            if ans:
                rx = ans[0][1]
                tx = ans[0][0]

                if rx.type == ICMP_TTL_EXC:
                    apariciones[rx.src] += 1.0
                    tiempo[rx.src] += (rx.time - tx.sent_time)

        if len(apariciones) >= 1:
            ip, veces_ip = apariciones.most_common(1)[0]
            tiempo = tiempo[ip] / veces_ip
        else:
            ip, tiempo = ("*", 0)

        return (ip, tiempo)

    def trace_route(self):
        ip_dst = self.ip_a_alcanzar()
        ttl = 1

        print('Trying to reach ip {}.'.format(ip_dst))

        while ttl <= self.hops:
            ip, rtt = self.nodo_a_distancia(ttl)
            ttl += 1

            print('{} ({}): {}'.format(socket.gethostbyaddr(ip), ip, rtt))
            if ip == ip_dst:
                print "Host reached."
                break
        else:
            print "Host not reached in {} hops".format(self.hops)

