#!/usr/bin/python
# -*-coding:utf-8 -*


from header import *
#from items import *
from perso import *
from carte import *
from world import *
#from mob import *


class Game:

	def __init__(self, number):

		self.continuer 	= 1
		self.number = number



		#Keep track of witch keyboard key is pressed
		self.pressed_keys = {	"north": 		False,
								"south":		False,
								"east":		False,
								"west":		False,
								"space":	False,
								"c":		False
								}
		#List the keyboard keys that can not be pressed too long. Key names have to be the same as pressed_keys dictionnary
		#self.max_key_duration = {	"up": 	0.1
									#}

		self.path = os.getcwd()
		self.saving_file = str(self.path) + "/save/save_" + str(self.number)

		self.world = World() #init world


	def Play(self, fenetre):
		# print("Game Playing!")
		self.start_turn_time = time.time()
		while self.continuer:
			self.PlayTurn()
			# print("Game Turn played")
			self.Display(fenetre)
			# print("Game displayed")

	def Display(self, fenetre):
		# print("Game displaying !")
		self.world.Display(fenetre)
		# print("\tWorld displayed")
		pygame.display.flip()


	def PlayTurn(self):
		self.IncrementPressedKeysDuration()
		self.world.PlayTurn(self)
		self.GetExternalEvents()
		self.EndTurn()

	def EndTurn(self):
		"""End the turn. For now : Pause the game a while for a certain fps"""
		time.sleep(max(0, g_turn_duration - (time.time() - self.start_turn_time)))
		self.start_turn_time = time.time()


	def IncrementPressedKeysDuration(self):
		"""Increment the time for every key that is curently being pressed"""
		for key in self.pressed_keys:
			if self.pressed_keys[key]:
				self.pressed_keys[key] += g_turn_duration
		#for key in self.max_key_duration:
			#self.pressed_keys[key] = min(self.pressed_keys[key], self.max_key_duration[key])



	def GetExternalEvents(self):
		for event in pygame.event.get():
			if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
				self.continuer=0

			elif event.type==KEYDOWN:
				if event.key == K_UP or event.key == K_z:
					self.pressed_keys["north"] = g_turn_duration
				elif event.key == K_DOWN or event.key == K_s:
					self.pressed_keys["south"] = g_turn_duration
				elif event.key==K_LEFT or event.key == K_q:
					self.pressed_keys["west"] = g_turn_duration
				elif event.key==K_RIGHT or event.key == K_d:
					self.pressed_keys["east"] = g_turn_duration
				elif event.key==K_SPACE:
					self.pressed_keys["space"] = g_turn_duration
				elif event.key==K_c:
					self.pressed_keys["c"] = g_turn_duration

			elif event.type==KEYUP:
				if event.key == K_UP or event.key == K_z:
					self.pressed_keys["north"] = False
				elif event.key == K_DOWN or event.key == K_s:
					self.pressed_keys["south"] = False
				elif event.key==K_LEFT or event.key == K_q:
					self.pressed_keys["west"] = False
				elif event.key==K_RIGHT or event.key == K_d:
					self.pressed_keys["east"] = False
				elif event.key==K_SPACE:
					self.pressed_keys["space"] = False
				elif event.key==K_c:
					self.pressed_keys["c"] = False
