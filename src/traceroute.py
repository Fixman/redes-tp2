import scapy.all as scp
import socket
from collections import Counter
ICMP_ECHO_REPLY = 0
ICMP_TIME_EXCEEDED = 11

def median(num):
    num.sort()
    if len(num) % 2 != 0:
        return num[len(num) / 2]

    return (num[len(num) / 2] + num[len(num) / 2 - 1]) / 2.

class RouteTracer:
    def __init__(self, dst, tries=10, hops=30, name=None):
        self.dst    = dst
        self.tries  = tries
        self.hops   = hops
        self.name   = name if name else dst

    def ip_a_alcanzar(self):
        pkt = scp.IP(dst=self.dst) / scp.ICMP()
        ans, _ = scp.sr(pkt, verbose=0)

        return ans[0][0].dst

    def nodo_a_distancia(self, ttl):
        # Devuelve la tupla (ip, rtt prom) del nodo a distancia ttl
    
        dst = self.dst
        pkt = scp.IP(dst=dst, ttl=ttl) / scp.ICMP()  
        dst_ip = pkt.dst

        hosts = Counter()
        times = {}

        for i in xrange(self.tries):
            ans, unans = scp.sr(pkt, verbose=0, timeout=1)

            if ans:
                rx = ans[0][1]
                tx = ans[0][0]

                if rx.type == ICMP_TIME_EXCEEDED or rx.type == ICMP_ECHO_REPLY:
                    hosts[rx.src] += 1
                    
                    if rx.src not in times:
                        times[rx.src] = []
                    times[rx.src] += [(rx.time - tx.sent_time) * 1000]
                    
        if hosts:
            best = hosts.most_common(1)[0][0]
            return (best, median(times[best]))

        return ('*', 0)

    def trace_route(self, verbose=False):
        ip_dst = self.ip_a_alcanzar()

        distance = -1
        nodes = []
        
        if verbose:
            print('Traceroute to {} ({}) with IP {}'.format(self.dst, self.name, ip_dst))

        for ttl in xrange(1, self.hops + 1):
            ip, rtt = self.nodo_a_distancia(ttl)
            host = '*'

            if ip != '*':
                try:
                    host = socket.gethostbyaddr(ip)[0]
                except socket.herror:
                    host = ip

            nodes += [{'ip': ip, 'host': host, 'rtt': rtt}]

            if verbose:
                print('{} {} ({}) {:.3f} ms'.format(ttl, host, ip, rtt))

            if ip == ip_dst:
                distance = ttl
                break

        if verbose:
            if distance != -1:
                print('Host reached in {} hops'.format(distance))
            else:
                print('Host not reached in {} hops'.format(self.hops))

        return (distance, nodes)
