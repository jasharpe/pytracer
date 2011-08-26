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
  def __init__(self, diffuse, specular, shininess, reflectivity):
    self.diffuse = diffuse
    self.specular = specular
    self.shininess = shininess
    self.reflectivity = reflectivity

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
  def __init__(self, resolution, origin, view_direction, up_direction, fov, ambient):
    self.children = []
    self.lights = []
    self.resolution = resolution
    self.origin = origin
    self.view_direction = view_direction
    self.up_direction = up_direction
    self.fov = fov
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

def load_scene(path):
  full_path = path + ".py"
  return imp.load_source(md5.new(full_path).hexdigest(), path + ".py", open(full_path, 'rb'))
