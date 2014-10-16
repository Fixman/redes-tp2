#! /usr/bin/python
# -*- coding: utf-8 -*-

import pylab

def rtt_grafico(mss, archivo):

    pylab.plot(mss, linewidth=2)

    pylab.xlim(0,len(mss))
    pylab.xlabel('Numero de HOP')
    pylab.ylabel('RTT (ms)')
    pylab.title('RTT en cada salto')
    
    pylab.tight_layout()
    pylab.savefig(archivo, format='pdf', orientation='landscape')
    pylab.clf()

def zscore_hist(zscores, archivo):

    pylab.hist(zscores, normed=True)

    pylab.xlabel('Zscore')
    pylab.ylabel('Porcentaje Apariciones')
    pylab.title('Distribucion de Zscore')
    
    pylab.tight_layout()
    pylab.savefig(archivo, format='pdf', orientation='landscape')
    pylab.clf()


def main():
    
    archivos = ["MSU","Oxford","Queensland","Tsinghua"]
    carpeta  = 'graficos/'

    for archivo in archivos:
        
        mss = []
        zscores = []

        with open(archivo,'r') as data:

            for linea in data:
                
                host, ip, rtt, zs = linea.split()
                mss.append(float(rtt))                 

                if host != '*':
                    zscores.append(float(zs))
      
        rtt_grafico(mss, carpeta + archivo + "_rtt")
        zscore_hist(zscores, carpeta + archivo + "_zscore")

if __name__=="__main__":    
    main()
