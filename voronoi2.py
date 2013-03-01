from PIL import Image
from random import randrange
from math import hypot
import t2b

def generate_voronoi_diagram(width, height, num_cells,ra,dec):
  image = Image.new("RGB", (width, height))
  putpixel = image.putpixel
  imgx, imgy = image.size
  nx = []
  ny = []
  nr = []
  ng = []
  nb = []

  for i in range(num_cells):
    (r,c)=t2b.RADECtoRowCol(ra[i],dec[i])
    nx.append(r)
    ny.append(c)
    nr.append(randrange(256))
    ng.append(randrange(256))
    nb.append(randrange(256))
  print "hola"
  for y in range(imgy):
    print y
    for x in range(imgx):
      dmin = hypot(imgx-1, imgy-1)
      j = -1
      for i in range(num_cells):
        d = hypot(nx[i]-x, ny[i]-y)
        if d < dmin:
          dmin = d
          j = i
      putpixel((x, y), (nr[j], ng[j], nb[j]))
  image.save("VoronoiDiagram.png", "PNG")
  image.show()


