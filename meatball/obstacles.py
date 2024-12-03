'''
Obstacle class
'''

import pygame 
import time

from setting import Setting

import random
import pygame

class Obstacle(pygame.sprite.Sprite):
   def __init__(self):
      pygame.sprite.Sprite.__init__(self)
      self.settings = Setting()
      self.height = 100
      self.x = self.settings.screen_width
      self.y = self.settings.screen_height - self.height
      self.speed = 7

      # Set a random delay before the obstacle starts moving
      self.delay_time = random.uniform(0, 1)  
      self.start_time = time.time() 

      # Obstacle types
      self.obstacle_types = {
         "scientist": self.load_images('scientist', 6),
         "scientist2": self.load_images('scientist2', 2),
         "robot": self.load_images('robot', 7)
      }

      # randomly select an obstacle type
      self.current_type = random.choice(list(self.obstacle_types.keys()))
      self.obstacle_images = self.obstacle_types[self.current_type]
      self.obstacle_images_index = 0

      # set initial sprite rect and position
      self.image = self.obstacle_images[int(self.obstacle_images_index)]
      self.rect = self.obstacle_images[self.obstacle_images_index].get_rect()
      self.y = self.settings.screen_height - self.rect.height
      self.rect.x = self.x
      self.rect.y = self.y

      self.mask = pygame.mask.from_surface(self.image) # create the mask for collision detection

   # load images for obstacles given to method
   def load_images(self, folder_name, size):
      images = []
      for i in range(size):
         image_path = f'/meatball/images/{folder_name}/0{i}_{folder_name}.png'
         image = pygame.image.load(image_path).convert_alpha()
         scale = self.height / image.get_height()
         new_width = int(image.get_width() * scale)
         new_height = int(image.get_height() * scale)
         image = pygame.transform.scale(image, (new_width, new_height))
         images.append(image)
      return images

   # draw current obstacle
   def draw(self):
      self.settings.screen.blit(self.obstacle_images[int(self.obstacle_images_index)], (self.x, self.y))

   # update obstacles position and animation
   def update(self):
      # only start moving after the random delay has passed
      current_time = time.time()
      if current_time - self.start_time >= self.delay_time:
         self.x -= self.speed 

      self.obstacle_images_index += 0.05
      if self.obstacle_images_index >= len(self.obstacle_images):
         self.obstacle_images_index = 0

      # update the rect for collision detection
      self.rect = self.obstacle_images[int(self.obstacle_images_index)].get_rect()
      self.rect.x = self.x
      self.rect.y = self.y
      self.mask = pygame.mask.from_surface(self.obstacle_images[int(self.obstacle_images_index)])

      # remove the item when it's off-screen
      if self.rect.x < -self.rect.width:
         self.kill() 
