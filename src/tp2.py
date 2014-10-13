from numpy import *
from traceroute import RouteTracer

hosts = [
    ('University of Oxford - Reino Unido', 'www.ox.ac.uk'),
    ('Universidade Estadual de Campinas - Brasil', 'www.unicamp.br'),
    ('The University of Queensland - Australia', 'uq.edu.au'),
    ('Massachussets Instutite of Technology - Estados Unidos', 'web.mit.edu'),
]

for university, host in hosts:
    distance, rtt_absolute = RouteTracer(host, name=university).trace_route(verbose=True)

    # No estoy contando el primer hop al router porque afea a todos los resultados.
    # Estoy asumiendo que quiero hacer todos los calculos, incluyendo el promedio y
    # desvio estandar, sobre las diferencias. Esta bien esto?
    rtt = diff(rtt_absolute[1:])
    
    N = len(rtt)
    mean = sum(rtt) / N
    stddev = sqrt(sum([(x - mean) ** 2 for x in rtt]) / N)
    zscore = [(x - mean) / stddev for x in rtt]

    print('{} {}:'.format(university, host))
    print('\tmean\t= {}'.format(mean))
    print('\tstddev\t= {}'.format(stddev))
    print('\tzscore\t=')
    for z in zscore:
        print ('\t\t{}'.format(z))
