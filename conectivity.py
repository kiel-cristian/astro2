import random as r

# class Matrix:
#   def _init_(self):

search_key = 1
no_search_key = 0
marker_key = '?'

matrix = []
dx = 0.2
dy = 0.1
# xoyo = (0.3,-1.234)
delta = 0.2
n = 20

def more_stars( i, j):
  if( matrix[j][i+1] == search_key or \
      matrix[j+1][i] == search_key or \
      matrix[j][i-1] == search_key or \
      matrix[j-1][i] == search_key or \
      matrix[j+1][i+1] == search_key or \
      matrix[j+1][i-1] == search_key or \
      matrix[j-1][i+1] == search_key or \
      matrix[j-1][i-1] == search_key) and matrix[j][i] == search_key:
    return True
  else:
    return False

def connect( n, dx, dy, delta = 0.2):
  for j in range(1,n-1):
    for i in range(1,n-1):
      connect_point( j, i, dx, dy, delta)

def connect_point( j, i, dx, dy, delta):
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

  while more_stars( control_i,control_j):
    if matrix[control_j-it_j][control_i] == search_key:
      if union( points, minx, maxx, miny, maxy, rx, ry, xcm, ycm, control_j-it_j, control_i, control_i, control_j, i , j):
        continue

    if matrix[control_j][control_i] == search_key:
      if union( points, minx, maxx, miny, maxy, rx, ry, xcm, ycm, control_j, control_i, control_i, control_j, i , j):
        continue

    if matrix[control_j+it_j][control_i] == search_key:
      if union( points, minx, maxx, miny, maxy, rx, ry, xcm, ycm, control_j+it_j, control_i, control_i, control_j, i , j):
        continue

    if matrix[control_j][control_i-it_i] == search_key:
      if union( points, minx, maxx, miny, maxy, rx, ry, xcm, ycm, control_j, control_i-it_i, control_i, control_j, i , j):
        continue

    if matrix[control_j][control_i+it_i] == search_key:
      if union( points, minx, maxx, miny, maxy, rx, ry, xcm, ycm, control_j, control_i+it_i, control_i, control_j, i , j):
        continue

def union( points, minx, maxx, miny, maxy, rx, ry, xcm, ycm, cj, ci, control_i, control_j, i , j):
  if matrix[cj][ci] == search_key:
    matrix[cj][ci] = marker_key
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

    if ycm < 0 or xcm <0 or xcm >= n or ycm >= n or rx >= delta or ry >= delta:
      return True
    else:
      matrix[control_j][control_i] = search_key
      return True
  else:
    return False

def print_matrix( n):
  p = ""
  for j in range(0,n):
    for i in range(0,n):
      p += "" + str( matrix[j][i])
    p += "\n"
  print(p)

def run():
  for i in range(0,n):
    row = []
    for j in range(0,n):
      if r.randint(0,1) == 1:
        row.append( search_key )
      else:
        row.append( no_search_key )

    matrix.append(row)

  print_matrix( n)
  connect( n, dx, dy, delta)
  print_matrix( n)


run()