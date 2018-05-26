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
		self.perso = Perso(self)


	def Display(self, fenetre):
		# print("World displaying !")
		self.world_map.Display(fenetre, self.perso.GetScreenPosition(), self.perso)
		# print("world_map displayed")
		self.perso.Display(fenetre)
		# print("Perso displayed")

	def PlayTurn(self, game):

		# start = time.time()
		# start_global = start
		self.perso.PlayTurn(game, self)
		# print("Perso", time.time() - start, 1. / (time.time() - start))
		# start = time.time()
		# print("World\t", time.time() - start, 1. / (time.time() - start))
		# print("Global\t", time.time() - start, 1. / (time.time() - start))
