from scene import Scene, Sphere, Light, Material
from geometry import Point

def get_scene():
  scene = Scene((255, 255, 255))
  scene.add_child(Sphere(Point(0, 0, 5), 1, Material((100, 0, 0), (100, 0, 0), 25)))
  scene.add_child(Sphere(Point(-0.1, 0.5, 3.75), 0.2, Material((0, 100, 0), (100, 0, 0), 25)))
  scene.add_light(Light(Point(-2, 2, 2), (255, 255, 255), (1, 0, 0)))
  return scene
