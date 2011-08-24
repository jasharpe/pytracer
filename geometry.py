import math

class Ray(object):
  def __init__(self, origin, direction):
    self.origin = origin
    self.direction = direction

class Point(object):
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z
    self.w = 1

  def __add__(self, v):
    if type(v) is Vector:
      return Point(self.x + v.x, self.y + v.y, self.z + v.z)
    raise TypeError()

  def __radd__(self, v):
    if type(v) is Vector:
      return Point(self.x + v.x, self.y + v.y, self.z + v.z)
    raise TypeError()

  def __sub__(self, p):
    if type(p) is Point:
      return Vector(self.x - p.x, self.y - p.y, self.z - p.z)
    raise TypeError()

  def __rsub__(self, p):
    if type(p) is Point:
      return p.__sub__(self)
    raise TypeError()

class Vector(object):
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z
    self.w = 0

  def __repr__(self):
    return "Vector(%f, %f, %f)" % (self.x, self.y, self.z)

  def __neg__(self):
    return Vector(-self.x, -self.y, -self.z)

  def __rmul__(self, s):
    if type(s) is int or type(s) is float:
      return Vector(self.x * s, self.y * s, self.z * s)
    elif type(s) is Vector:
      return s.__mul__(self)
    raise TypeError()

  def __mul__(self, s):
    if type(s) is int or type(s) is float:
      return Vector(self.x * s, self.y * s, self.z * s)
    elif type(s) is Vector:
      v = Vector(
          self.y * s.z - self.z * s.y,
          self.z * s.x - self.x * s.z,
          self.x * s.y - self.y * s.x
      )
      return v
    raise TypeError()

  def __add__(self, v):
    if type(v) is Vector:
      return Vector(self.x + v.x, self.y + v.y, self.z + v.z)
    raise TypeError()

  def __radd__(self, v):
    if type(v) is Vector:
      return v.__add__(self)
    raise TypeError()

  def __sub__(self, v):
    if type(v) is Vector:
      return Vector(self.x - v.x, self.y - v.y, self.z - v.z)
    raise TypeError()

  # return a vector representing the reflection of this vector in the plane
  # described by normal.
  def reflect(self, normal):
    v = self.normalize()
    n = normal.normalize()
    return (self - 2 * v.dot(n) * n).normalize()

  def dot(self, v):
    if type(v) is Vector:
      return self.x * v.x + self.y * v.y + self.z * v.z
    raise TypeError()

  def length2(self):
    return self.dot(self)

  def length(self):
    return math.sqrt(self.dot(self))

  def normalize(self):
    length = math.sqrt(self.dot(self))
    if length == 0:
      raise Exception("Attempted to normalize 0 vector")
    return Vector(self.x / length, self.y / length, self.z / length)
