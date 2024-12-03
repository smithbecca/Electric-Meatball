'''
Item class
'''

import pygame
import random

from setting import Setting

# item image path
item_path = '/meatball/images/item.png'

class Item(pygame.sprite.Sprite):
   def __init__(self):
      super().__init__()
      self.settings = Setting()
      self.height = 100
      self.speed = 7

      # load image
      self.image = pygame.image.load(item_path).convert_alpha()
      scale = self.height / self.image.get_height()
      new_width = self.image.get_width() * scale
      new_height = self.image.get_height() * scale
      self.image = pygame.transform.scale(self.image, (new_width, new_height))

      # spawn off screen and give random y position
      self.rect = self.image.get_rect()
      self.rect.x = random.randint(self.settings.screen_width, self.settings.screen_width + 500)
      self.rect.y = random.randint(50, self.settings.screen_height - 50)

   # move item to the left and remove when off screen
   def update(self):
      self.rect.x -= self.speed 
      if self.rect.x < -self.rect.width:
         self.kill()
