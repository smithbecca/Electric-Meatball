'''
Meatball class
'''

import pygame
import sys 
import math
import random

from setting import Setting
from player import Player
from obstacles import Obstacle
from item import Item

# image paths
background_image = '/meatball/images/pixel_lab.png'
win_path = '/meatball/images/new_brain.png' 
man_path = '/meatball/images/01_Bite.png'

class Meatball:
   def __init__(self):
      pygame.init()
      self.settings = Setting()
      self.player = Player()
      self.score_to_win = 50

      # game variables
      self.speed_const = 6
      self.obstacles_group = pygame.sprite.Group()
      self.items_group = pygame.sprite.Group()
      self.spawn_obstacle()
      self.spawn_item()

      self.clock = pygame.time.Clock()
      self.font = self.settings.font

      # fade variables
      self.fade_alpha = 0
      self.fade_speed = 5
      self.fading = False 

      # brain image for winning screen 
      self.winning_image = pygame.image.load(win_path).convert()
      win_desired_width = 330
      win_desired_height = 240
      self.winning_image = pygame.transform.scale(self.winning_image, (win_desired_width, win_desired_height))
      self.winning_image_rect = self.winning_image.get_rect()
      self.winning_image_rect.center = (self.settings.screen_width // 2 + 100, (self.settings.screen_height // 2 + 50))

      # sprite image for winning screen
      self.man_winning = pygame.image.load(man_path).convert_alpha()
      man_desired_width = 300
      man_desired_height = 300
      self.man_winning = pygame.transform.scale(self.man_winning, (man_desired_width, man_desired_height))
      self.man_winning_rect = self.man_winning.get_rect()
      self.man_winning_rect.center = (self.settings.screen_width // 2 - 250, (self.settings.screen_height // 2 + 100))

   # spawn a new item at a random location
   def spawn_item(self):
      item = Item()
      self.items_group.add(item)
   
   # check if player collides with item
   def check_item_collision(self):
      collided_items = pygame.sprite.spritecollide(self.player, self.items_group, True)
      if collided_items:
         self.settings.score += 1
   
   # spawn new obstacle and add it to the group
   def spawn_obstacle(self):
        self.obstacle = Obstacle()
        self.obstacle.speed = self.speed_const
        self.obstacles_group.add(self.obstacle)

   # increase the fade effect until screen is fully black
   def update_fade(self):
      if self.fading:
         if self.fade_alpha < 255:
            self.fade_alpha += self.fade_speed 
         else:
            self.fade_alpha = 255
   
   # draw the fade to the surface
   def draw_fade(self):
      fade_surface = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
      fade_surface.fill((0, 0, 0)) 
      fade_surface.set_alpha(self.fade_alpha) 
      self.settings.screen.blit(fade_surface, (0, 0)) 

   def _check_events(self):
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            self.running = False
            sys.exit()
         if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.player.jump()

   def continue_game(self):
      for event in pygame.event.get():
            if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()
            # get the player's input (Y or N)
            if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_y:
                  # restart game
                  meatball = Meatball()
                  meatball.run_game()
               elif event.key == pygame.K_n:
                  # exit game
                  pygame.quit()
                  sys.exit()

   def check_collision(self):
      if pygame.sprite.spritecollide(self.player, self.obstacles_group, True, pygame.sprite.collide_mask):
         if self.player.health > 1:
            self.player.health -= 1
            self.player.invincibility_frame = 30
            self.spawn_obstacle()
         else:
            event_string = 'Game over. Play again? (Enter Y or N)'
            self.event_screen(event_string)
         
   def define_parallax(self):
      # background image
      self.lab = pygame.image.load(background_image).convert()
      self.num_bg_tiles = math.ceil(self.settings.screen_width / self.lab.get_width()) + 1

      self.bgs = []
      self.bgs.append(pygame.image.load(background_image).convert())
      self.parallax = []
      for x in range(len(self.bgs)):
         self.parallax.append(0)

   def update_parallax(self):
      for i in range(self.num_bg_tiles):
         self.settings.screen.blit(self.lab, (i * self.lab.get_width(), 0))
         
      for i in range(len(self.bgs)):
         bg = self.bgs[i]
         for j in range(self.num_bg_tiles):
            self.settings.screen.blit(bg, (j * bg.get_width() + self.parallax[i], 0))

      # update speed for parallax effect
      for i in range(len(self.parallax)):
         self.parallax[i] -= i + 2
         if abs(self.parallax[i]) > self.bgs[i].get_width():
            self.parallax[i] = 0

   # shows score in top right corner
   def show_score(self):
      self.black = (0, 0, 0)
      font = pygame.font.Font(pygame.font.get_default_font(), 24)
      text = font.render(f'Score: {self.settings.score}', True, self.black)
      text_rect = text.get_rect()
      text_rect.center = (self.settings.screen_width - 80, 30)
      self.settings.screen.blit(text, text_rect)

   # reusable function for game over and winning screen
   def event_screen(self, event_string):
      event = True
      color = (62, 125, 187)
      while event:
         pygame.draw.rect(self.settings.screen, color, (0, 50, self.settings.screen_width, 100))
         font = pygame.font.Font(pygame.font.get_default_font(), 22)
         text = font.render(event_string, True, self.black)
         text_rect = text.get_rect()
         text_rect.center = (self.settings.screen_width / 2, 100)
         self.settings.screen.blit(text, text_rect)

         pygame.display.update()

         self.continue_game()

   def run_game(self):
      self.running = True
      self.define_parallax()
      self.player.init_heart()
      while self.running:
         self.clock.tick(self.settings.fps)
         self._check_events()
         self.player._update_screen()
         self.check_collision()
         self.check_item_collision()

         # randomly spawn items at intervals
         if random.randint(0, 1000) < 2:
            self.spawn_item()

         self.items_group.update()

          # update all obstacles
         for obstacle in self.obstacles_group:
            obstacle.update()
            
            # reset obstacle if it moves off-screen
            if obstacle.x < obstacle.rect.width * -1:
               self.settings.score += 1
               # increase obstacle speed
               if self.settings.score % 2 == 0 and obstacle.speed < 10:
                  obstacle.speed += 0.5
                  self.speed_const = obstacle.speed
               elif self.settings.score % 3 == 0 and (self.settings.score > 20 and obstacle.speed >= 10):
                  obstacle.speed += .75
                  self.speed_const = obstacle.speed
               self.obstacles_group.remove(obstacle)
               self.spawn_obstacle()

         # set item speed to match obstacle's speed
         for item in self.items_group:
            item.speed = self.speed_const

         # fill with background 
         self.settings.screen.fill(self.settings.bg_color)  
         self.update_parallax()
         self.items_group.draw(self.settings.screen)

         for obstacle in self.obstacles_group:
            obstacle.draw()
         
         self.player.draw()
         self.player.draw_hearts()
         self.show_score()
         
         # check if the score has reached needed number to go to winning menu
         if self.settings.score == self.score_to_win and not self.fading:
            self.fading = True 
         
         if self.fading:
            self.update_fade()
            self.draw_fade()

            # check if fade is done
            if self.fade_alpha >= 255:  
               pygame.time.delay(1000)
               self.settings.screen.blit(self.winning_image, self.winning_image_rect)
               self.settings.screen.blit(self.man_winning, self.man_winning_rect)
               event_string = 'You escaped the lab! Wanna go back in? (Enter Y or N)'
               self.event_screen(event_string)

         pygame.display.flip()

meatball = Meatball()
meatball.run_game()
