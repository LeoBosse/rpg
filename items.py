#!/usr/bin/python
# -*-coding:utf-8 -*
##!/usr/local/bin/python3

from header import *

class Inventory:

	def __init__(self, size_max = 10):
		self.max_size = size_max
		self.list=[]

		self.rect=pygame.Rect(LONGUEUR_FENETRE/4, HAUTEUR_FENETRE/4, LONGUEUR_FENETRE/2, HAUTEUR_FENETRE/2)
		self.colour_bkg=(50, 50, 50)

	def Afficher(self, fenetre):
		fenetre.fill(self.colour_bkg, self.rect)

	def AddObject(self, object):
		if len(self.list) < self.max_size:
			self.list.append(object)
			return True
		else:
			return False

	def GetWeight(self):
		w = 0
		for o in self.list:
			w += o.weight
		return w



class Object:

	def __init__(self, name, attack=0, defense=0, weight=0, cut_wood=False, speed_bonus=0):

		self.name			= name
		self.attack 		= attack
		self.defense		= defense
		self.weight			= weight
		self.cut_wood		= cut_wood
		self.speed_bonus	= speed_bonus

class Weapons(Object):

	def __init__(self, name, atk, defense, weight):
		Object.__init__(name)
		self.atk=atk
		self.defense=defense
		self.weight=weight

class Sword(Weapons):

	def __init__(self, name, atk, defense, weight, cut_wood):
		Weapons.__init__(name, atk, defense, weight)
		self.cut_wood=cut_wood

class Shield(Weapons):

	def __init__(self, name, atk, defense, weight):
		Weapons.__init__(name)

class Axe(Weapons):

	def __init__(self, name, atk, defense, weight, cut_wood):
		Weapons.__init__(name)
		self.cut_wood=cut_wood
