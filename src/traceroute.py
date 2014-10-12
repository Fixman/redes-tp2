import scapy.all as scp
from collections import Counter
ICMP_TTL_EXC = 11

class RouteTracer:

    def __init__(self, dst, times=15, hops=30):
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
            ans, unans = scp.sr(pkt, verbose=0, timeout=0.4)

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
        hops = self.hops
        ttl = 1
        alcanzado = False

        while not alcanzado and ttl <= hops:
            ip, rtt = self.nodo_a_distancia(ttl)
            alcanzado = (ip == ip_dst)
            ttl += 1

            print('{}: {}'.format(ip, rtt))

        if alcanzado:
            print "Host reached."
        else:
            print "Host not reached in {} hops".format(self.hops)

