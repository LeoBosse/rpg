#!/usr/bin/python
# -*-coding:utf-8 -*
##!/usr/local/bin/python3


from header import *
from perso import *
from carte import *

class World:
	def __init__(self, load = False):
		self.time 		= 0
		# self.gravity	= 80 #gravity force pulling everything down (defined positive)

		self.nb_lines	= NB_CELLS_WORLD_X
		self.nb_columns		= NB_CELLS_WORLD_Y


		# self.InitBioms()

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



# 	def InitBioms(self):
# 		"""Initialize all bioms. Return a list of all of them to be used by world_map and Ligns creation. All parameters should have obvious names"""
# 		self.biom_list = [Biom({"name":					"default",
# 						"air_image":			pygame.image.load("images/air_small.bmp").convert(),
# 						"ground_image":			pygame.image.load("images/herbe.bmp").convert(),
# 						"under_ground_image":	pygame.image.load("images/terre_small.bmp").convert(),
# 						"tree_image":			pygame.image.load("images/arbre.bmp").convert(),
# 						"average_slope": 		0.3,
# 						"slope_continuity":		10,
# 						"tree_probability":		0.3
#
# 		})]
#
# 		self.biom_list.append(Biom({"name":					"desert",
# 						"air_image":			pygame.image.load("images/air_small.bmp").convert(),
# 						"ground_image":			pygame.image.load("images/sand_small.bmp").convert(),
# 						"under_ground_image":	pygame.image.load("images/sand_small.bmp").convert(),
# 						"tree_image":			pygame.image.load("images/arbre.bmp").convert(),
# 						"average_slope": 		0.3,
# 						"slope_continuity":		10,
# 						"tree_probability":		0.3
#
# 		}))
#
# class Biom:
#
# 	def __init__(self, dic):
# 		"""Initialize a biom from a dictionnary"""
# 		self.name						= dic["name"]
#
# 		self.air_image					= dic["air_image"]
# 		self.ground_image				= dic["ground_image"]
# 		self.under_ground_image 		= dic["under_ground_image"]
# 		self.under_ground_shadow_image 	= pygame.image.load("images/noir_small.bmp").convert()
# 		self.tree_image					= dic["tree_image"]
#
# 		self.average_slope				= dic["average_slope"]					#What is the average difference of altitude beween two line. in numbers of cells.
# 		self.slope_continuity			= dic["slope_continuity"]				#How long before changing slope. in numbers of cells.
#
# 		self.tree_prbability			= dic["tree_probability"]
