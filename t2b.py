# -*- coding: utf-8 -*-
import pyfits as pf
import pylab as pl
import scipy as sp
import numpy as np
from math import *
from scipy import random

if __file__:
  debug = True
else:
  debug = False

maxROW = 1000
maxCOL = 1000

hdulist = pf.open('newimage2.fits')
hdu= hdulist[0].data
h=hdu.ravel()

crpix1=hdulist[0].header['CRPIX1']
crpix2=hdulist[0].header['CRPIX2']
crval1=hdulist[0].header['CRVAL1']
crval2=hdulist[0].header['CRVAL2']
cd1_1=hdulist[0].header['CD1_1']
cd1_2=hdulist[0].header['CD1_2']
cd2_1=hdulist[0].header['CD2_1']
cd2_2=hdulist[0].header['CD2_2']

def getRa(ROW,COL):
	ra = cd1_2*(ROW-crpix2)+cd1_1*(COL-crpix1)+crval1
	return (ra)

def getDec(ROW,COL):
	dec = cd2_2*(ROW-crpix2)+cd2_1*(COL-crpix1)+crval2
	return (dec)

def gaussian(x,stdev,mean):

    return np.exp(-1.0*(x-mean)**2.0/(2*stdev**2.0))/(stdev*np.sqrt(2*np.pi))

def get_p_value(value_list,stdev,mean):

	x    = np.min(value_list)
	eps  = 10#10**-3/(stdev*np.sqrt(2*np.pi))   este paso esta en 10 solo para que el codigo corra mas rapido, cambiarlo para la version final
	num  = len(value_list)
	pval = np.zeros(len(value_list))

	while True:

		gval = gaussian(x,stdev,mean)
		#print x, gval
		if x > 0 and gval <10**-10:break #< eps: break
		for i in range(num):
			dint = gval * eps
			if x >= value_list[i]:
				pval[i] += dint
		x += eps

	return pval

def FDR_method(data,alpha,mean2,stdev2):
	N = len(data)
	pvals = get_p_value(data,stdev2,mean2)

	pvals_and_pos = []
	for i in range(N):
		pvals_and_pos.append((pvals[i],i))

	pvals_and_pos.sort()

	diff = np.zeros(N)
	for i in range(N):
		j  = i + 1
		pj = pvals_and_pos[i][0]
		diff[i] += pj - (j * alpha)/(1.0 * N)

	indx = -1
	for i in range(N):
		if diff[i] < 0.0:
			indx = i

	if indx == -1: return []


	pval_c = pvals_and_pos[indx][0]

	if debug:
		print pval_c

	source_pos = []
	for i in range(N):
		if pvals_and_pos[i][0] <= pval_c:
			pos = pvals_and_pos[i][1]
			source_pos.append(pos)

	return source_pos

#pos_sources = FDR_method(h,0.5,1000.0,20.0)

def matrizDeteciones(data,pos_sources):
	detecciones = np.zeros(len(data))

	for i in range(len(pos_sources)):
		detecciones[pos_sources[i]]=1

	detecciones2=detecciones.reshape(maxROW,-1)
	return detecciones2

def getRaDec(detecciones3):

	RA=[]
	DEC=[]

	for i in range(maxROW):
		for j in range(maxCOL):
			if detecciones3[i][j] == 1: #modificar por el radio de la psf y no pixel exacto
				RA.append(getRa(i,j))
				DEC.append(getDec(i,j))
	return (RA,DEC)

def RADECtoRowCol(RA,DEC):
	row = 1/(cd1_2*cd2_1-cd1_1*cd2_2)*(cd2_1*(RA-crval1)-cd1_1*(DEC-crval2))+crpix2
	col = 1/(cd1_2*cd2_1-cd1_1*cd2_2)*(-cd2_2*(RA-crval1)+cd1_2*(DEC-crval2))+crpix1
	return (int(row),int(col))#revisar bien esto despues

def addStar2(hdu, RA, DEC):
	(ROW,COL) = RADECtoRowCol(RA,DEC)
	if 0 <= ROW < maxROW and 0 <= COL < maxCOL:
		hdu[ROW,COL] =1
	return

def addStellarCatalog2(hdu, catalog):
	for linea in open(catalog):
		linea = linea.strip()
		obj, ra, dec,mag,sed,index,tipo = linea.split()
		ra = float(ra)
		dec = float(dec)
		addStar2(hdu,ra,dec)
	return

def addGalaxy2(hdu, m, RA, DEC, n, Re, el, theta):
	(ROW,COL)=RADECtoRowCol(RA,DEC)
	if 0 <= ROW < maxROW and 0 <= COL < maxCOL:
		a1=int(ROW-5*Re)
		b1=int(ROW+5*Re)
		a2=int(COL-5*Re)
		b2=int(COL+5*Re)
		for y in range(a1,b1):
			for x in range(a2,b2):
				if 0 <= y < maxROW and 0 <= x < maxCOL:
					#hdu[y,x] += psersic(Re,n,m,COL,ROW,x,y,el,theta)
					hdu[y,x]=1
	return

def addGalaxyCatalog2(hdu, catalog):
	i=0
	for linea in open(catalog):
		linea = linea.strip()
		obj, ra, dec,mag,sed,redshift,tipo,n,re,elip,o = linea.split()
		ra = float(ra)
		dec = float(dec)
		mag = float(mag)
		n = float(n)
		re = float(re)
		elip = float(elip)
		o = float(o)
		addGalaxy2(hdu,mag,ra,dec,n,re,elip,o)
		i += 1
		#if i > 200: break
	return

# TODO
def detectWithPsf(hdu,i,j,psf):
	return hdu[j][i]


if debug:
	# los prints que siguen son solo para tener una idea de que el codigo esta haciendo lo que se supone que haga
	print len(h), len(pos_sources)
	print detecciones2.shape
	print detecciones2[2,0],detecciones[maxROW*2]
	print len(RA),len(DEC)