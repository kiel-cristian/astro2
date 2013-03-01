from random import randint
from math import sqrt
from numpy import *

class Matrix:
  def __init__(self, n, N, delta, search_key=1, no_search_key=0, matrix= None):
    self.search_key = 1
    self.no_search_key = 0
    self.marker_key = -2.0
    self.star_marker = -1.0
    self.delta = delta
    self.n = n
    self.N = N
    self.matrix = []
    self.matrix_list = []
    self.matrix_copy = []

    if matrix == None:
      self.__init_matrix__()
    else:
      self.matrix = matrix[:] #copy editable inner matrix

    self.matrix_copy = self.matrix[:] #backup matrix


  def __init_matrix__(self):
    for i in range(0,self.n):
      row = []
      for j in range(0,self.n):
        if randint(0,1) == 1:
          row.append( self.search_key )
        else:
          row.append( self.no_search_key )
        self.matrix_list.append([j,i])
      self.matrix.append(row)

  def __set_control_vars__(self, j, i):
    #Temporal global variables
    ##
    self.xcm = i
    self.ycm = j
    ###
    self.minx = i
    self.miny= j
    ###
    self.maxx = i
    self.maxy= j
    ###
    self.rx= 0
    self.ry= 0
    self.r = 0

    self.points = 0
    self.union_points = []
    self.next_point = False

  def valid_point(self,j,i):
    return j >= 0 and j < self.n and i >= 0 and i < self.n

  def more_stars(self, i, j):
    if( self.matrix[j][i+1] == self.search_key or \
        self.matrix[j+1][i] == self.search_key or \
        self.matrix[j][i-1] == self.search_key or \
        self.matrix[j-1][i] == self.search_key):
      return True
    else:
      return False

  def has_a_star(self, j, i):
    if self.valid_point( j, i ):
      return self.matrix[j][i] == self.search_key
    else:
      return False

  def can_expand(self, j = None, i = None):
    if j == None or i == None:
      return self.r < self.delta and self.points <= self.N
    else:
      return self.has_a_star( j, i) and self.valid_point( j, i) and self.r < self.delta and self.points <= self.N

  def connect(self):
    self.matrix = self.matrix_copy

    # Randomized version
    # l = self.matrix_list[:] #copy list
    # while len(l) > 0:
    #   index = randint(0,len(l)-1)
    #   j = l[index][0]
    #   i = l[index][1]
    #   self.connect_point(j,i)
    #   del(l[index])

    # Lineal implementation version
    for j in range(0,self.n):
      for i in range(0,self.n):
        self.connect_point( j, i)

    if not debug:
      for j in range(0,self.n):
        for i in range(0,self.n):
          self.clean_marker( j, i)
    return self.matrix

  def clean_marker(self,j,i):
    if self.matrix[j][i] == self.star_marker or self.matrix[j][i] == self.marker_key:
      self.matrix[j][i] = self.search_key

  def connect_point(self, j, i):
    if not self.has_a_star(j,i):
      return

    self.__set_control_vars__( j, i)
    self.connect_recursive( j, i)
    self.unify_points()

  def connect_recursive(self,j,i):
    if self.union( j, i):

      # Randomized implementation
      # dirs = []
      # d = randint(0,3)
      # dirs += [d]
      # while len(dirs) < 4:
      #   d = randint(0,3)
      #   if not(d in dirs):
      #     dirs += [d]

      # Iterative implementation
      dirs = [0,1,2,3]

      for d in dirs:
        if d == 0:
          self.connect_recursive( j+1, i)
        elif d == 1:
          self.connect_recursive( j, i-1)
        elif d == 2:
          self.connect_recursive( j-1, i)
        elif d == 3:
          self.connect_recursive( j, i+1)

  def union(self, cj, ci):
    if self.can_expand( cj, ci):
      self.points += 1

      if ci < self.minx:
        self.minx = ci
      if ci > self.maxx:
        self.maxx = ci

      if cj < self.miny:
        self.miny = cj
      if cj > self.maxy:
        self.maxy = cj

      self.rx =  (self.maxx - self.minx) + 1
      self.ry = (self.maxy - self.miny) + 1
      self.r = sqrt(self.rx**2 + self.ry**2)/2

      self.matrix[cj][ci] = self.marker_key # mark the united point
      self.union_points.append([cj,ci])
      return True
    else:
      return False

  def unify_points(self):
    if self.points >= self.N:
      xcm = 0
      ycm = 0

      for point in self.union_points:
        y = point[0]
        x = point[1]

        self.matrix[y][x] = self.no_search_key #delete the united point

        ycm += y
        xcm += x

      xcm = int(round( xcm / self.points))
      ycm = int(round( ycm / self.points))

      self.xcm = xcm
      self.ycm = ycm

      self.matrix[self.ycm][self.xcm] = self.star_marker
    # points < N
    else:
      for point in self.union_points:
        y = point[0]
        x = point[1]

        self.matrix[y][x] = self.marker_key #delete the united point
      self.matrix[self.ycm][self.xcm] = self.search_key

  def print_m(self):
    p = ""
    for j in range(0,self.n):
      for i in range(0,self.n):
        p += "  " + str( self.matrix[j][i])
      p += "\n"
    print(p)

def run():
  n = 40
  delta = 3
  N = 4

  matrix = Matrix( n = n, N = N, delta = delta)

  matrix.print_m()
  matrix.connect()
  matrix.print_m()

if __name__ == '__main__':
  run()