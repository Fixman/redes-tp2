from traceroute import RouteTracer

hosts = [
    ('Universita degli study di Milano - Italia', 'www.unimi.it'),
    ('The University of Queensland - Australia', 'uq.edu.au'),
    ('Massachussets Instutide of Technology - EEUU', 'web.mit.edu'),
    ('Keio University - Japon', 'www.keio.ac.jp'),
]

for university, host in hosts:
    print('Traceroute to {} ({}):'.format(university, host))
    RouteTracer(host).trace_route()
