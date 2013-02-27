import random as r

class Matrix:
  def __init__(self, n, delta, search_key=1, no_search_key=0):
    self.search_key = 1
    self.no_search_key = 0
    self.marker_key = '?'
    self.delta = delta
    self.n = n
    self.matrix = []

    self.__init_matrix__()
    self.connected_matrix = []

  def __init_matrix__(self):
    for i in range(0,self.n):
      row = []
      for j in range(0,self.n):
        if r.randint(0,1) == 1:
          row.append( self.search_key )
        else:
          row.append( self.no_search_key )
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

    self.points = 0

  def valid_point(self,j,i):
    return j >= 0 and j < self.n and i >= 0 and i < self.n

  def more_stars(self, i, j):
    if( self.matrix[j][i+1] == self.search_key or \
        self.matrix[j+1][i] == self.search_key or \
        self.matrix[j][i-1] == self.search_key or \
        self.matrix[j-1][i] == self.search_key or \
        self.matrix[j+1][i+1] == self.search_key or \
        self.matrix[j+1][i-1] == self.search_key or \
        self.matrix[j-1][i+1] == self.search_key or \
        self.matrix[j-1][i-1] == self.search_key):
      return True
    else:
      return False

  def has_a_star(self, j, i):
    if self.valid_point( j, i ):
      return self.matrix[j][i] == self.search_key
    else:
      return False

  def can_expand(self):
    return self.ycm >= 0 and self.xcm >=0 and self.xcm < self.n and self.ycm < self.n and self.rx < self.delta and self.ry < self.delta

  def connect(self):
    for j in range(1,self.n-1):
      for i in range(1,self.n-1):
        self.connect_point( j, i)

  def connect_point(self, j, i):
    self.__set_control_vars__( j, i)

    while self.more_stars( i = self.xcm, j = self.ycm) and self.can_expand():
      print("xcm: " + str(self.xcm))
      print("ycm: " + str(self.ycm))

      for dj in range(-1,2):
        cj = self.ycm+dj
        for di in range(-1,2):
          ci = self.xcm+di

          if self.can_expand():
            if self.has_a_star( j = cj, i = ci):
              self.union( cj, ci)

      self.print_m()

  def union(self, cj, ci):
    self.points += 1

    if ci < self.minx:
      self.minx = ci
    if ci > self.maxx:
      self.maxx = ci

    if cj < self.miny:
      self.miny = cj
    if cj > self.maxy:
      self.maxy = cj

    self.rx =  self.maxx - self.minx
    self.ry = self.maxy - self.miny

    self.move_mass_center( cj= cj, ci= ci)

  def move_mass_center(self, cj, ci):
    new_xcm = (self.xcm*(self.points - 1) + (ci))/(self.points)
    new_ycm = (self.ycm*(self.points - 1) + (cj))/(self.points)

    if self.valid_point( j=new_ycm, i=new_xcm):

      self.matrix[cj][ci] = self.marker_key
      self.matrix[self.ycm][self.xcm] = self.marker_key

      dx = self.xcm - new_xcm
      dy = self.ycm - new_ycm

      if self.xcm == new_xcm:
        print("xcm no vario en :" + str(new_xcm))
      else:
        print("cambiando xcm a:" + str(new_xcm))

      # if self.ycm == new_ycm:
      #   print("ycm no vario en :" + str(new_ycm))
      # else:
      #   print("cambiando ycm a:" + str(new_ycm))

      self.xcm = new_xcm
      self.ycm = new_ycm

      ###
      self.minx += dx
      self.miny += dy
      ###
      self.maxx += dx
      self.maxy += dy
      ###

      self.matrix[self.ycm][self.xcm] = self.search_key

  def print_m(self):
    p = ""
    for j in range(0,self.n):
      for i in range(0,self.n):
        p += "  " + str( self.matrix[j][i])
      p += "\n"
    print(p)

def run():
  n = 10
  delta = 3
  matrix = Matrix( n= n, delta= delta)

  matrix.print_m()
  matrix.connect()
  matrix.print_m()

run()