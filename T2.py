import pyfits as pf
import pylab as pl
import scipy as sp
import numpy as np
from math import *
from scipy import random
import t2b 

hdulist = pf.open('newimage2.fits')
h1= hdulist[0].data
h2=h1.ravel()


def FindFDR(hdu,sigma_noise,fdr,N,psf):

	pos_sources = t2b.FDR_method(hdu,fdr,1000.0,sigma_noise)
	detecciones = np.zeros(len(hdu))
	M=t2b.matrizDeteciones(hdu,pos_sources)
# por aca en algun lado hay que usar lo de conectividad
	(r,d)=t2b.getRaDec(M)#esto genera los vectores ra y dec que se piden, pero creo tiene que ser con los objetos detectados despues de la conectividad no estoy seguro, de ser asi necesitaria un par de modificaciones
 
	matrizlista=np.zeros([4096,4096])
	catalogo1="stellar.dat"
	catalogo2="galaxy.dat"
	t2b.addStellarCatalog2(matrizlista,catalogo1)
	t2b.addGalaxyCatalog2(matrizlista,catalogo2)
	# esto crea una matriz de 1s y 0s (matrizlista) deacuerdo a las posiciones de los catalogos de la tarea 1 para ver las detecciones falsas, de momento en el casi de las galaxias solo marca el centro pero es facil hacer que ponga 1 en toda la extensionde la galaxia si fuese necesrio

	reales=0#contador de el numero de detecciones que son reales
	for i in range(4096):
		for j in range(4096):
			if M[i][j] == 1 :# aca quizas haya que reempazar las matriz M que se genra antes por los objetos que quedan despues de la conectividad
				if matrizlista[i][j] == 1 :#aca falta agregar que se busque un objeto en el radio de la psf y no en la coordenada exacta
					reales +=1
	print reales, len(pos_sources) - reales, (len(pos_sources) - reales)/len(pos_sources)
	return (r,d,M)

(ra,dec,detec)=FindFDR(h2,20.0,0.05,10,2)

print len(ra),len(dec),detec.shape

# aca falta agregar todo lo de la parte 2				
	
