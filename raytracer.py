import pygame, math
from geometry import Point, Vector, Ray

def multiplier(fov, value, max_value):
  return math.tan(fov * (value - max_value / 2.0) / max_value)

def average_colors(colors):
  return map(lambda x: float(x) / len(colors), reduce(lambda x, y: map(lambda (a, b): a + b, zip(x, y)), colors, (0, 0, 0)))

class Raytracer(object):
  def calculate_color(self, ray, intersection, scene):
    ambient = scene.ambient
    diffuse = intersection.obj.material.diffuse
    specular = intersection.obj.material.specular
    shininess = intersection.obj.material.shininess

    color = map(lambda (x, y): x * y / 255.0, zip(ambient, diffuse))
    for light in scene.lights:
      point = intersection.position
      light_direction = (light.position - point).normalize()
      light_distance2 = (light.position - point).length2()
      
      # check if shadowed
      shadow = self.cast_ray(Ray(point, light_direction), scene)
      if not shadow is None and (shadow.position - point).length2() < light_distance2:
        continue

      dist = (light.position - point).length()
      attenuation = 1 / (light.falloff[0] + light.falloff[1] * dist + light.falloff[2] * dist * dist)
      l_dot_n = light_direction.dot(intersection.normal)

      reflected = ray.direction.reflect(intersection.normal).normalize()
      r_dot_v = reflected.dot(light_direction)
      for i in xrange(0, 3):
        lighting = 0
        # diffuse
        if l_dot_n > 0:
          lighting += diffuse[i] * l_dot_n * light.color[i] / 255.0
        if r_dot_v > 0:
          lighting += specular[i] * (r_dot_v ** shininess) * light.color[i] / 255.0
        if lighting > 0:
          color[i] += lighting * attenuation

    return map(lambda x: min(255, x), color)
  
  def cast_ray(self, ray, scene):
    intersections = scene.intersect(ray)
    if not intersections:
      return None
    else:
      closest = None
      closest_dist = 0
      for intersection in intersections:
        dist = (intersection.position - ray.origin).length()
        if closest is None or closest_dist > dist:
          closest = intersection
          closest_dist = dist
      return closest

  def trace(self, scene, aa=False):
    original_resolution = scene.resolution
    if aa:
      resolution = map(lambda x: 2 * x, scene.resolution)
    fov_radians = scene.fov * math.pi / 180.0
    image = pygame.Surface(resolution)
    x_direction = (scene.view_direction.normalize() * scene.up_direction.normalize()).normalize()
    up_direction = -scene.up_direction.normalize()
    for x in xrange(0, resolution[0]):
      target_x = x_direction * multiplier(fov_radians, x, resolution[0])
      if x % 100 == 0:
        print x
      for y in xrange(0, resolution[1]):
        target_y = up_direction * multiplier(fov_radians, y, resolution[1])
        direction = (target_x + target_y + Vector(0, 0, -1)).normalize()
        ray = Ray(scene.origin, direction)
        intersection = self.cast_ray(ray, scene)
        if intersection is not None:
          color = self.calculate_color(ray, intersection, scene)
          
          # do reflections
          reflected_component = intersection.obj.material.shininess / 100.0
          current_ray = ray
          current_intersection = intersection
          while reflected_component > 0.01:
            reflection_ray = current_ray.direction.reflect(current_intersection.normal)
            current_ray = Ray(current_intersection.position, reflection_ray)
            current_intersection = self.cast_ray(current_ray, scene)
            if current_intersection is None:
              break
            ref_color = self.calculate_color(current_ray, current_intersection, scene)
            for i in xrange(0, 3):
              color[i] = min(255, color[i] + reflected_component * ref_color[i])
            reflected_component *= current_intersection.obj.material.shininess / 100.0
          
          image.set_at((x, y), color)
        else:
          bg_color = (0, 0, 255 * y / float(resolution[1]))
          image.set_at((x, y), bg_color)
    if aa:
      aa_image = pygame.Surface(original_resolution)
      for x in xrange(0, original_resolution[0]):
        for y in xrange(0, original_resolution[1]):
          color = average_colors([
              image.get_at((2 * x, 2 * y)),
              image.get_at((2 * x + 1, 2 * y)),
              image.get_at((2 * x, 2 * y + 1)),
              image.get_at((2 * x + 1, 2 * y + 1))
          ])
          aa_image.set_at((x, y), color)
      return aa_image
    else:
      return image
