#!/usr/bin/python3.5
# -*-coding:utf-8 -*
# #
from classes.header import *

# from classes.items import *
from classes.perso import *
from classes.carte import *
#
# #from mob import *
# from classes.editor import *


class World:
	def __init__(self, load = False):
		self.time 		= 0

		self.nb_lines	= NB_CELLS_WORLD_X
		self.nb_columns	= NB_CELLS_WORLD_Y

		self.world_map = World_Map(self)
		self.perso = Perso()
		self.PNGs = [PNG("alice", pos=(int(WORLD_WIDTH/2) + 30, int(WORLD_HEIGHT/2) + 30))]


	def Display(self, fenetre):
		# print("World displaying !")
		self.world_map.Display(fenetre, self.GetScreenPosition(), self.perso)
		# print("world_map displayed")
		self.perso.Display(fenetre)
		for i, png in enumerate(self.PNGs):
			png.Display(fenetre, png.GetPositionOnScreen(self.GetScreenPosition()))
		# print("Perso displayed")

	def PlayTurn(self, pressed_keys):

		# start = time.time()
		# start_global = start
		self.perso.PlayTurn(pressed_keys, self)
		for i, png in enumerate(self.PNGs):
			if png.IsOnscreen(self.GetScreenPosition()):
				self.world_map.InoccupyCell(png)
				png.Move(pressed_keys, self)
				self.world_map.OccupyCell(png)
				if m.sqrt((png.rect.centerx - self.perso.rect.centerx)**2 + (png.rect.centery - self.perso.rect.centery)**2) < 100:
					png.Speak()
				else:
					png.speaking =  False

		# print("Perso", time.time() - start, 1. / (time.time() - start))
		# start = time.time()
		# print("World\t", time.time() - start, 1. / (time.time() - start))
		# print("Global\t", time.time() - start, 1. / (time.time() - start))


	def GetScreenPosition(self):
		"""Get screen position in the world from the perso position"""
		xs = self.perso.rect.x - self.perso.position_on_screen[0]
		ys = self.perso.rect.y - self.perso.position_on_screen[1]
		return (xs, ys)
