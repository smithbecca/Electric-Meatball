"""
Setting class
"""
import pygame

class Setting:
	def __init__(self):
		self.screen_width = 960
		self.screen_height = 540
		self.score = 0
		self.bg_color = (230, 230, 230)
		self.fps = 60
		self.font = pygame.font.Font(pygame.font.get_default_font(), 16)
		self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
		pygame.display.set_caption('Electric Meatball')