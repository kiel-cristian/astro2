# -*- coding: utf-8 -*-
import pyfits as pf
import pylab as pl
import scipy as sp
import numpy as np
from math import *
from scipy import random


maxROW = 4096
maxCOL = 4096
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
    print x, gval
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

  print pval_c

  source_pos = []
  for i in range(N):
    if pvals_and_pos[i][0] <= pval_c:
      pos = pvals_and_pos[i][1]
      source_pos.append(pos)

  return source_pos

pos_sources = FDR_method(h,0.5,1000.0,20.0)
detecciones = np.zeros(len(h))

for i in range(len(pos_sources)):
  detecciones[pos_sources[i]]=1

detecciones2=detecciones.reshape(4096,-1)

RA=[]
DEC=[]

for i in range(4096):
  for j in range(4096):
    if detecciones2[i][j] == 1:
      RA.append(getRa(i,j))
      DEC.append(getDec(i,j))



# los prints que siguen son solo para tener una idea de que el codigo esta haciendo lo que se supone que haga
print len(h), len(pos_sources)
print detecciones2.shape
print detecciones2[2,0],detecciones[4096*2]
print len(RA),len(DEC)


