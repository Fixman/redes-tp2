#!/usr/bin/python

from traceroute import RouteTracer


def main():

    #Universit\`a degli studi di milano - Italia
    tr = RouteTracer('www.unimi.it')
    tr.trace_route()

    #The University of Queensland - Australia
    tr = RouteTracer('uq.edu.au')
    tr.trace_route()

    #MIT - EEUU
    tr = RouteTracer('web.mit.edu')
    tr.trace_route()

    #Keio University - Japon
    tr = RouteTracer('www.keio.ac.jp')
    tr.trace_route()

    
if __name__=="__main__":
    main()
