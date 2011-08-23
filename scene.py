import md5
import os.path
import imp
import traceback
import sys, math
from geometry import Vector, Point

class Light(object):
  def __init__(self, position, color, falloff):
    self.position = position
    self.color = color
    self.falloff = falloff

class Intersection(object):
  def __init__(self, position, normal, obj):
    self.position = position
    self.normal = normal
    self.obj = obj

class Material(object):
  def __init__(self, diffuse, specular, shininess):
    self.diffuse = diffuse
    self.specular = specular
    self.shininess = shininess

class Sphere(object):
  def __init__(self, position, radius, material):
    self.position = position
    self.radius = radius
    self.material = material

  def intersect(self, ray):
    intersections = set()
    
    o_to_o = ray.origin - self.position
    B = o_to_o.dot(ray.direction)
    C = o_to_o.dot(o_to_o) - self.radius ** 2
    descr = B * B - C
    if descr > 0:
      t = -B - math.sqrt(descr)
      if t > 0.0001:
        position = ray.origin + t * ray.direction
        normal = (position - self.position).normalize()
        intersections.add(Intersection(position, normal, self))
    return intersections

class Scene(object):
  def __init__(self, ambient):
    self.children = []
    self.lights = []
    self.ambient = ambient

  def add_child(self, child):
    self.children.append(child)

  def add_light(self, light):
    self.lights.append(light)

  def intersect(self, ray):
    intersections = set()
    for child in self.children:
      intersections |= child.intersect(ray)
    return intersections

def load_module(code_path):
  try:
    try:
      code_dir = os.path.dirname(code_path)
      code_file = os.path.basename(code_path)
      fin = open(code_path, 'rb')
      return  imp.load_source(md5.new(code_path).hexdigest(), code_path, fin)
    finally:
      try: fin.close()
      except: pass
  except ImportError, x:
    traceback.print_exc(file = sys.stderr)
    raise
  except:
    traceback.print_exc(file = sys.stderr)
    raise

def load_scene(path):
  return load_module(path + ".py")
