from traceroute import RouteTracer

hosts = [
    ('Universidade Estadual de Campinas', 'www.unicamp.br'),
    ('Universita degli study di Milano - Italia', 'www.unimi.it'),
    ('The University of Queensland - Australia', 'uq.edu.au'),
    ('Massachussets Instutite of Technology - EEUU', 'web.mit.edu'),
]

for university, host in hosts:
    print('Traceroute to {} ({}):'.format(university, host))
    RouteTracer(host).trace_route()
