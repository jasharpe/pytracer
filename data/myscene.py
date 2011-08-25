from scene import Scene, Sphere, Light, Material
from geometry import Point, Vector

def get_scene():
  scene = Scene((500, 500), Point(0, 0, 800), Vector(0, 0, -1), Vector(0, 1, 0), 45, (0.3, 0.3, 0.3))
  mat1 = Material((0.7, 1.0, 0.7), (0.5, 0.7, 0.5), 25, 0.25)
  mat2 = Material((0.5, 0.5, 0.5), (0.5, 0.7, 0.5), 25, 0.25)
  mat3 = Material((1.0, 0.6, 0.1), (0.5, 0.7, 0.5), 25, 0.25)
  mat4 = Material((0.7, 0.6, 1.0), (0.5, 0.4, 0.8), 25, 0.25)

  # s1
  scene.add_child(Sphere(Point(0, 0, -400), 100, mat1))
  # s2
  scene.add_child(Sphere(Point(200, 50, -100), 150, mat1))
  # s3
  scene.add_child(Sphere(Point(0, -1200, -500), 1000, mat2))
  # b1 (TODO)
  # s4
  scene.add_child(Sphere(Point(-100, 25, -300), 50, mat3))
  # s5
  scene.add_child(Sphere(Point(0, 100, -250), 25, mat1))

  # white light
  scene.add_light(Light(Point(-100, 150, 400), (0.9, 0.9, 0.9), (1, 0, 0)))
  # orange light
  scene.add_light(Light(Point(400, 100, 150), (0.7, 0.0, 0.7), (1, 0, 0)))
  return scene
