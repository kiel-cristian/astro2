import pyfits as pf
import pylab as pl
import scipy as sp
import numpy as np
from math import *
from scipy import random
from t2b import *
from connectivity import *

if __file__:
  debug = True
else:
  debug = False

hdulist = pf.open('newimage2.fits')
h1= hdulist[0].data
h2=h1.ravel()

def FindFDR(hdu,sigma_noise,fdr,N,psf):

	pos_sources = FDR_method(hdu,fdr,1000.0,sigma_noise)
	detecciones = np.zeros(len(hdu))
	M = vmatrizDeteciones(hdu,pos_sources)

	# conectividad
	M2 = Matrix( n = maxROW, N = N, delta = psf, matrix = M).connect()

	#esto genera los vectores ra y dec que se piden,
	#pero creo tiene que ser con los objetos detectados despues de la conectividad no estoy seguro,
	#de ser asi necesitaria un par de modificaciones
	(r,d)=getRaDec(M)

	matrizlista=np.zeros([maxROW,maxCOL])
	catalogo1="stellar.dat"
	catalogo2="galaxy.dat"
	addStellarCatalog2(matrizlista,catalogo1)
	addGalaxyCatalog2(matrizlista,catalogo2)
	# esto crea una matriz de 1s y 0s (matrizlista) deacuerdo a las posiciones de los catalogos de la tarea 1 para ver las detecciones falsas, de momento en el casi de las galaxias solo marca el centro pero es facil hacer que ponga 1 en toda la extensionde la galaxia si fuese necesrio

	reales=0#contador de el numero de detecciones que son reales
	for i in range(maxROW):
		for j in range(maxCOL):
			if M[i][j] == 1 :# aca quizas haya que reempazar las matriz M que se genra antes por los objetos que quedan despues de la conectividad
				if matrizlista[i][j] == 1 :#aca falta agregar que se busque un objeto en el radio de la psf y no en la coordenada exacta
					reales +=1
	if debug:
		print reales, len(pos_sources) - reales, (len(pos_sources) - reales)/len(pos_sources)
	return (r,d,M)

(ra,dec,detec)=FindFDR(hdu=h2,sigma_noise=20.0,fdr=0.05,N=10,psf=2)

if debug:
	print len(ra),len(dec),detec.shape

# aca falta agregar todo lo de la parte 2
