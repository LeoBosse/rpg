#!/usr/bin/python3.5
# -*-coding:utf-8 -*

from classes.header import *
# from classes.perso import *
# from classes.carte import *
# from classes.world import *
# from classes.game import *
# #from mob import *
# from classes.editor import *


class Inventory:

	def __init__(self, size_max = 10):
		self.max_size = size_max
		self.list=[]

		self.rect=pygame.Rect(NB_PIX_SCREEN_X/4, NB_PIX_SCREEN_Y/4, NB_PIX_SCREEN_X/2, NB_PIX_SCREEN_Y/2)
		self.colour_bkg=(50, 50, 50)


	def Display(self, fenetre, mode, pos=(0,0)):

		x, y = pos

		if not self.IsEmpty():
			if   mode == "cell":
				self.list[0].Display(fenetre, pos)

			elif mode == "plain":
				fenetre.fill(self.colour_bkg, self.rect)
				for i, item in enumerate(self.list):
					item.Display(fenetre, (self.rect.x + ITEM_WIDTH * i, self.rect.y + ITEM_HEIGHT * (i / (self.rect.w / ITEM_WIDTH))))
					# fenetre.blit(item.GetImage(), (self.rect.x + ITEM_WIDTH * i, self.rect.y + ITEM_HEIGHT * (i / (self.rect.w / ITEM_WIDTH))))

	def Open(self, fenetre, mode="plain"):
		self.Display(fenetre, mode)
		pygame.display.flip()
		continuer = True
		while continuer:
			for event in pygame.event.get():
				if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
					continuer = False


	def IsEmpty(self):
		return len(self.list) == 0


	def AddItem(self, object):
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
	def __repr__(self):
		"""Quand on entre notre objet dans l'interpréteur"""
		return str(self.list)





class Item:
	def __init__(self, name, weight, attack=0, defense=0, cut_wood=False, speed_bonus=0):

		self.name			= name
		self.weight			= weight
		self.attack 		= attack
		self.defense		= defense
		self.cut_wood		= cut_wood
		self.speed_bonus	= speed_bonus
		self.image_name		= "I_ITEM"

	def GetImage(self):
		return images_dict[self.image_name]

	def Display(self, fenetre, pos):
		fenetre.blit(self.GetImage(), pos)

class Weapon(Item):
	def __init__(self, name, weight, attack, defense, cut_wood=False):
		Item.__init__(self, name, weight, attack=attack, defense=defense, cut_wood=cut_wood)


class Sword(Weapon):
	def __init__(self, name, weight, attack, defense, cut_wood=True):
		Weapon.__init__(self, name, weight, attack, defense, cut_wood=cut_wood)
		self.image_name = "I_SWORD"

class Shield(Weapon):
	def __init__(self, name, weight, atk, defense):
		Weapons.__init__(self, name)


class Axe(Weapon):
	def __init__(self, name, weight, atk, defense, cut_wood):
		Weapons.__init__(self, name)
		self.cut_wood = cut_wood
