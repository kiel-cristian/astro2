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

  def more_stars(self, i, j):
    if( self.matrix[j][i+1] == self.search_key or \
        self.matrix[j+1][i] == self.search_key or \
        self.matrix[j][i-1] == self.search_key or \
        self.matrix[j-1][i] == self.search_key or \
        self.matrix[j+1][i+1] == self.search_key or \
        self.matrix[j+1][i-1] == self.search_key or \
        self.matrix[j-1][i+1] == self.search_key or \
        self.matrix[j-1][i-1] == self.search_key) and self.matrix[j][i] == self.search_key:
      return True
    else:
      return False

  def connect(self):
    for j in range(1,self.n-1):
      for i in range(1,self.n-1):
        self.connect_point( j, i)

  def connect_point(self, j, i):
    if j < 0 or i < 0:
      return

    xcm = i
    ycm = j

    control_i = i
    control_j = j

    minx = i
    miny= j

    maxx = i
    maxy= j

    rx= 0
    ry= 0

    points = 0
    end = False

    it_j = 1
    it_i = 1

    while self.more_stars( control_i,control_j):
      if self.matrix[control_j-it_j][control_i] == self.search_key:
        if self.union( points, minx, maxx, miny, maxy, rx, ry, xcm, ycm, control_j-it_j, control_i, control_i, control_j, i , j):
          continue

      if self.matrix[control_j][control_i] == self.search_key:
        if self.union( points, minx, maxx, miny, maxy, rx, ry, xcm, ycm, control_j, control_i, control_i, control_j, i , j):
          continue

      if self.matrix[control_j+it_j][control_i] == self.search_key:
        if self.union( points, minx, maxx, miny, maxy, rx, ry, xcm, ycm, control_j+it_j, control_i, control_i, control_j, i , j):
          continue

      if self.matrix[control_j][control_i-it_i] == self.search_key:
        if self.union( points, minx, maxx, miny, maxy, rx, ry, xcm, ycm, control_j, control_i-it_i, control_i, control_j, i , j):
          continue

      if self.matrix[control_j][control_i+it_i] == self.search_key:
        if self.union( points, minx, maxx, miny, maxy, rx, ry, xcm, ycm, control_j, control_i+it_i, control_i, control_j, i , j):
          continue

  def union(self, points, minx, maxx, miny, maxy, rx, ry, xcm, ycm, cj, ci, control_i, control_j, i , j):
    if self.matrix[cj][ci] == self.search_key:
      self.matrix[cj][ci] = self.marker_key
      points += 1

      if ci < minx:
        minx = ci
      if ci > maxx:
        maxx = ci

      if cj < miny:
        miny = cj
      if cj > maxy:
        maxy = cj

      rx =  maxx - minx
      ry = maxy - miny

      xcm = (xcm*(points - 1) + (ci))/(points)
      ycm = (ycm*(points - 1) + (control_j + j))/(points)

      control_j = int(ycm)
      control_i = int(xcm)

      if ycm < 0 or xcm <0 or xcm >= self.n or ycm >= self.n or rx >= self.delta or ry >= self.delta:
        return True
      else:
        self.matrix[control_j][control_i] = self.search_key
        return True
    else:
      return False

  def print_m(self):
    p = ""
    for j in range(0,self.n):
      for i in range(0,self.n):
        p += "" + str( self.matrix[j][i])
      p += "\n"
    print(p)

def run():
  n = 20
  delta = 3
  matrix = Matrix( n= n, delta= delta)

  matrix.print_m()
  matrix.connect()
  matrix.print_m()

run()