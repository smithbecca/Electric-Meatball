'''
Player class
'''
import pygame

from setting import Setting

# sprite image paths
heart_path = '/meatball/images/heart.png'

class Player(pygame.sprite.Sprite):
   def __init__(self):
      pygame.sprite.Sprite.__init__(self)
      self.settings = Setting()
      self.height = 300
      self.x = 25
      self.y = self.settings.screen_height - self.height
      self.ground_level = self.settings.screen_height - self.height
      self.action = 'running'
      self.health = 3

      # load running sprites
      self.running_sprites = []
      self.running_sprite_index = 0
      for i in range(7):
         running_sprite = pygame.image.load(f'/meatball/images/Run/0{i}_Run.png').convert_alpha()
         scale = self.height / running_sprite.get_height()
         new_width = running_sprite.get_width() * scale
         new_height = running_sprite.get_height() * scale
         running_sprite = pygame.transform.scale(running_sprite, (new_width, new_height))
         self.running_sprites.append(running_sprite)

      # load the jumping sprites
      self.jumping_sprites = []
      self.jumping_sprite_index = 0
      for i in range(8):
         jumping_sprite = pygame.image.load(f'/meatball/images/Jump/0{i}_Jump.png').convert_alpha()
         scale = self.height / jumping_sprite.get_height()
         new_width = jumping_sprite.get_width() * scale
         new_height = jumping_sprite.get_height() * scale
         jumping_sprite = pygame.transform.scale(jumping_sprite, (new_width, new_height))
         self.jumping_sprites.append(jumping_sprite)

      # set initial sprite rect
      self.rect = self.running_sprites[self.running_sprite_index].get_rect()
      self.rect.x = self.x
      self.rect.y = self.y

      # number of frames 
      self.invincibility_frame = 0

   # draw the sprite based on the character action and index
   def draw(self):
      if self.action == 'running':
         running_sprite = self.running_sprites[int(self.running_sprite_index)]

         # invinciblity effect when you run into an obstacle
         if self.invincibility_frame > 0:
            self.invincibility_frame -= 1
         if self.invincibility_frame % 10 == 0:
            self.settings.screen.blit(running_sprite, (self.x, self.y))

      elif self.action == 'jumping' or self.action == 'landing':
         jumping_sprite = self.jumping_sprites[int(self.jumping_sprite_index)]

         # invinciblity effect when you run into an obstacle
         if self.invincibility_frame > 0:
            self.invincibility_frame -= 1
         if self.invincibility_frame % 10 == 0:
            self.settings.screen.blit(jumping_sprite, (self.x, self.y))

   # update the sprite index so next sprite image is drawn, increment by 0.1 so it takes 5 frames to get to the next index
   def _update_screen(self):
      if self.action == 'running':
         self.running_sprite_index += 0.175
         if self.running_sprite_index >= len(self.running_sprites):
            self.running_sprite_index = 0
         self.rect = self.running_sprites[int(self.running_sprite_index)].get_rect()
         self.rect.x = self.x
         self.rect.y = self.y
         self.mask = pygame.mask.from_surface(self.running_sprites[int(self.running_sprite_index)]) # update mask for collision detection

      elif self.action == 'jumping' or self.action == 'landing':
         self.jumping_sprite_index += 0.08
         if self.action == 'jumping':
            self.y -= 3
            if self.y <= self.settings.screen_height - self.height * 1.4:
               self.action = 'landing'
         elif self.action == 'landing':
            self.y += 3
            if self.y >= self.ground_level:
               self.y = self.ground_level
               self.jumping_sprite_index = 0
               self.action = 'running'
         
         self.rect = self.jumping_sprites[int(self.jumping_sprite_index)].get_rect()
         self.rect.x = self.x
         self.rect.y = self.y
         self.mask = pygame.mask.from_surface(self.jumping_sprites[int(self.jumping_sprite_index)]) # update mask for collision detection
      pygame.display.update()
   
   # make player go to jumping action
   def jump(self):
      if self.action not in ['jumping', 'landing']:
         self.action = 'jumping'

   # initializes hearts on screen
   def init_heart(self):
      self.heart = pygame.image.load(heart_path)
      scale = 80 / self.heart.get_width()
      new_width = self.heart.get_width() * scale
      new_height = self.heart.get_height() * scale
      self.heart = pygame.transform.scale(self.heart, (new_width, new_height))

   # set heart placement on screen
   def draw_hearts(self):
      for life in range(self.health):
         x_pos = 30 + life * (self.heart.get_width() + 15)
         y_pos = 5 
         self.settings.screen.blit(self.heart, (x_pos, y_pos))
      