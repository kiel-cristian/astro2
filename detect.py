from math import sqrt,pi
from numpy import *

class Detect:
  def __init__(self, j, i, delta):
    self.center = [j,i]
    self.neighbours = []

    self.r = 0.0
    self.area = 0.0
    self.delta = delta

  def add_neighbour(self,j,i):
    r = self.get_distance(j,i)
    if r >= self.delta or [j,i] == self.center:
      return False
    else:
      if not([j,i] in self.neighbours):
        self.neighbours.append([j,i])
        self.r = r
        self.area = pi*self.r**2/2
        return True
      else:
        return False

  def get_distance(self, pj, pi):
    dy = (pj - self.center[0]) + 1
    dx = (pi - self.center[1]) + 1
    return sqrt(dx**2 + dy**2)/2

  def print_info(self):
    print("center: [x,y]=" + str(self.center))

    for neighbour in self.neighbours:
      print(" -> neighbour: [x,y]=" + str(neighbour))

def run():
  d = Detect(j=0,i=0,delta=2)

  print(str(d.add_neighbour(j=1,i=1)) + str(": Should be True")) #should be True
  print(str(d.add_neighbour(j=0,i=0)) + str(": Should be False because center is unique")) #should be True
  print(str(d.add_neighbour(j=1,i=1)) + str(": Should be False by uniqueness")) #should be False, by uniqueness
  print(str(d.add_neighbour(j=3,i=3)) + str(": Should be False by exceed")) #should be False, area exceed limit
  print(str(d.add_neighbour(j=0,i=1)) + str(": Should be True by no variance")) #should be True, no limits variance
  print(str(d.add_neighbour(j=4,i=4)) + str(": Should be False by exceed")) #should be False, area exceed limit

  print("neighbours: " + str(d.neighbours))
  print("area: " + str(d.area))
  print("r: " + str(d.r))
  d.print_info()

if __name__ == '__main__':
  run()
