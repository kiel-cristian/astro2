from random import randint
from math import sqrt
from numpy import *
from detect import *
from t2b import *
from conectivity import *

#RADECtoRowCol

class Cummule:
  def __init__(self, n, ra, dec, delta, matrix):
    self.detects = []
    self.matrix = matrix[:] #matrix copy
    self.n = n
    self.ra = ra
    self.dec = dec
    self.delta = delta
    self.search_key = 1
    self.no_search_key = 0
    self.marker_key = -1

    self.mark_assigned_cummules()
    self.load_not_connected_elements()
    self.clear_marks()

  def clear_marks(self):
    for i in range(0,self.n):
      for j in range(0,self.n):
        if self.matrix[i][j] == self.marker_key:
          self.matrix[i][j] = self.search_key

  def mark_assigned_cummules(self):
    for i in range(0,len(self.ra)):
      ra = self.ra[i]
      dec = self.dec[i]
      point = RADECtoRowCol(ra,dec)
      x = point[0]
      y = point[1]
      if self.valid_point(y,x):
        self.matrix[x][y] = self.marker_key

  def not_assigned_to_cummule(self,j,i):
    return self.matrix[i][j] != self.marker_key

  def load_not_connected_elements(self):
    for i in range(0,self.n):
      for j in range(0,self.n):
        val = self.matrix[j][i]

        if val == self.search_key and self.not_assigned_to_cummule(j,i):
          self.load_boundary(j,i)

    self.sort_detects()

  def load_boundary(self,j,i):
    d = Detect(j=j,i=i,delta=self.delta)

    for di in range(i-self.delta,i+self.delta+1):
      #(y-j)**2 = r**2 - (x-i)**2
      limit =  int(round(sqrt(self.delta**2 - (di -i)**2)))

      #sup part
      for dj in range(j,j+limit+1):
        if self.valid_point(dj,di) and self.matrix[di][dj] == self.search_key:
          d.add_neighbour(i=di,j=dj)

      #inf part
      for dj in range(j,j-limit-1):
        if self.valid_point(dj,di) and self.matrix[di][dj] == self.search_key:
          d.add_neighbour(i=di,j=dj)

    self.detects.append(d)

  def sort_detects(self):
    self.detects = sorted(self.detects, key=self.custom_key)

  def custom_key(self,detect):
    detect.area

  def get_elements(self, x):
    for i in range(1,x+1):
      self.detects[i].print_info()

  def valid_point(self,j,i):
    if j < 0 or j >= self.n or i>=self.n or i < 0:
      return False
    else:
      return True

if __name__ == '__main__':
  n = 4096
  delta = 3
  N = 8

  m = Matrix( n = n, N = N, delta = delta)

  if n <= 100:
    m.print_m()

  print("Connecting matrix")
  m2 = m.connect()

  print("Calculating Ra Dec")
  (ra,dec) = getRaDec(m2)

  print("Initializing cummules")
  c = Cummule(n, ra, dec, delta, m2) #only for testing

  print("Printing elements")
  c.get_elements()


