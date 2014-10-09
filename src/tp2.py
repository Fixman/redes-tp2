#!/usr/bin/python

from traceroute import TraceRouter


def main():
    tr = TraceRouter('google.com.ar')
    ip_dst = tr.ip_a_alcanzar()

    ttl = 1
    alcanzado = False

    while not alcanzado:

        ip, rtt = tr.nodo_a_distancia(ttl)
        alcanzado = (ip == ip_dst)
        ttl += 1

        print (ip, rtt)

    print "HOST REACHED"
if __name__=="__main__":
    main()
