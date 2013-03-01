from random import randint
from math import sqrt
from numpy import *
from detect import *

if __file__:
  debug = True
else:
  debug = False

class Cummule:
  def __init__(self, n, matrix):
    self.detects = []