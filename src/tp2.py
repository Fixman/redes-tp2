from numpy import *
from traceroute import RouteTracer

hosts = [
    ('Moscow State University - Rusia', 'www.msu.ru', 'MSU'),
    ('Tsinghua University - China', 'www.tsinghua.edu.cn', 'Tsinghua'),
    ('University of Oxford - Reino Unido', 'www.ox.ac.uk', 'Oxford'),
    ('The University of Queensland - Australia', 'uq.edu.au', 'Queensland'),
]

for university, host, shortname in hosts:
    f = open('../results/{}'.format(shortname), mode='w')
    distance, nodes = RouteTracer(host, name=university).trace_route(verbose=True)

    # No estoy contando el primer hop al router porque afea a todos los resultados.
    nodes = [x for x in nodes if 'cab.prima.net.ar' not in x['host']][1:]

    # Estoy asumiendo que quiero hacer todos los calculos, incluyendo el promedio y
    # desvio estandar, sobre las diferencias. Esta bien esto?
    rtt = [0] + diff([x['rtt'] for x in nodes]).tolist()

    N = len(rtt)
    mean = sum(rtt) / N
    stddev = sqrt(sum([(x - mean) ** 2 for x in rtt]) / N)
    zscore = [(x - mean) / stddev for x in rtt]

    print('{} {}:'.format(university, host))
    print('\tmean\t= {}'.format(mean))
    print('\tstddev\t= {}'.format(stddev))
    print('\tzscore\t=')
    for n, z in enumerate(zscore):
        print ('\t\t{:.3f}\t{} ({})'.format(z, nodes[n]['host'], nodes[n]['ip']))
        f.write('{:.3f} {:.3f} {}\n'.format(z, rtt[n], nodes[n]['host']))

    f.close()
