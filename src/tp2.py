import numpy
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

    # No estoy contando el primer hop al router.
    nodes = nodes[1:]

    # Calculo la diferencia entre todos los que contestaron
    contestaron = [x['rtt'] for x in nodes if x['ip'] != '*']
    rtt = [contestaron[0]] + numpy.diff(contestaron).tolist()

    mean = numpy.mean(rtt)
    stddev = numpy.std(rtt)
    zscore = [(x - mean) / stddev for x in rtt]

    print('{} {}:'.format(university, host))
    print('\tmean\t= {}'.format(mean))
    print('\tstddev\t= {}'.format(stddev))
    print('\tzscore\t=')

    i=0
    for n in nodes:

        if n['ip'] != '*':
            zs, host, ip, rtt = zscore[i], n['host'], n['ip'], n['rtt']
            i += 1

            print   '\t\t{}\t({})\t{:.3f}\t{:.3f}'.format(host, ip, rtt, zs)
            f.write('{}\t({})\t{:.3f}\t{:.3f}\n'.format(host, ip, rtt, zs))
        else:
            print ('\t\t*\t(*)\t0\t*')
            f.write('*\t(*)\t0\t*\n')

    f.close()
