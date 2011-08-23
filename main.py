import sys, pygame, os
from raytracer import Raytracer
from scene import load_scene

def main(argv):
  raytracer = Raytracer()
  scene = load_scene(os.path.join("data", argv[1]))
  image = raytracer.trace(scene.get_scene(), (512, 512), 50)
  pygame.image.save(image, os.path.join("results", argv[1] + ".png"))

if __name__ == "__main__":
  main(sys.argv)