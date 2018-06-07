#!/usr/bin/python3.5
# -*-coding:utf-8 -*
# #
from classes.header import *
from classes.items import *
# from classes.carte import *
# from classes.world import *
# from classes.game import *
# #from mob import *
# from classes.editor import *

class Character:
	"""Classe de character, personnage, etre animés : informations, mouvement..."""
	def __init__(self, name="default", pos=(0,0)):
		"""init le perso, son fichier et son inventaire"""

		self.name = name

		self.speed			= 0
		self.speeds			= [0, 0] #speed [east+/west-, up+/down-]
		self.direction		= -1 #-1: not moving, 0: south, 1: east, 2:north, 3:west

		self.text_file		= "data/text/" + name
		self.speech_index	= 0
		try:
			self.speech_list	= open(self.text_file, "r").read().split("\n\n")
		except:
			self.speech_list	= open(self.text_file, "a").close()
			self.speech_list	= open(self.text_file, "r").read().split("\n\n")

		self.speech_list	= [i for i in self.speech_list if i]
		# for i in range(len(self.speech_list)):
		# 	if not self.speech_list[- 1 - i]:
		# 		del self.speech_list[- 1 - i]
		# self.speech_list	= [i.replace("\\", "\n") for i in self.speech_list]
		# print(self.speech_list)
		self.speaking		= False
		self.speech			= ""
		self.speech_rect	= pygame.Rect(0,0,0,0)

		self.images_folder	= "data/images/characters/"
		self.image			= "I_PNG"
		self.animation_lenght= 1
		self.animation_speed = 0.5
		self.frame_counter = 0
		self.images_list	= [[self.image],[self.image],[self.image],[self.image]]

		self.image_width	= 10
		self.image_height	= 20

		self.rect		= pygame.Rect(pos[0], pos[1], self.image_width, self.image_height)
		self.mass		= 1

		self.inventory = Inventory()

		self.vision		= 100					#Maximum distance the perso can see by default (in pixels)

	def GetPositionOnScreen(self, screen_position=(0,0)):
		return self.rect.x - screen_position[0], self.rect.y - screen_position[1]


	def Speak(self):
		self.speaking = True
		self.speech = self.GetSpeechLine()
		self.speech = [font.render(s.strip(), True, (0,0,0), (255,255,255)) for s in self.speech]
		# w, h = font.size(self.speech)

		# self.speech_rect = pygame.Rect(self.rect.centerx - w / 2, self.rect.top - h, w, h)


	def GetSpeechLine(self):
		if self.speech_index < len(self.speech_list):
			return self.speech_list[self.speech_index].replace("\0", "").split("\\n")
		else:
			return ""


	def PlayTurn(self, pressed_keys, world):
		self.Move(pressed_keys, world)

	def GetVisionRadius(self):
		"""Return the furthest distance the perso can see (in pixels). Should take object into account for the future"""
		return self.vision

	def CalculateSpeedFromExternalEvents(self, pressed_keys):
		"""Get the speed of Perso, from the presed directional keys."""

		if pressed_keys["east"] and not pressed_keys["west"]:
			self.speeds[0] = self.speed
			self.direction = 1
		elif pressed_keys["west"] and not pressed_keys["east"]:
			self.speeds[0] = -self.speed
			self.direction = 3
		else:
			self.speeds[0] = 0
			self.direction = -1

		if pressed_keys["south"] and not pressed_keys["north"]:
			self.speeds[1] = self.speed
			self.direction = 0
		elif pressed_keys["north"] and not pressed_keys["south"]:
			self.speeds[1] = -self.speed
			self.direction = 2
		else:
			self.speeds[1] = 0
			if self.direction != 1 and self.direction != 3:
				self.direction = -1

	def OpenInventory(self, fenetre):
		self.inventory.Open(fenetre)


	def GetImage(self):
		if self.direction >= 0:
			self.frame_counter += 1
			return images_dict[self.images_list[self.direction][int(self.frame_counter * self.animation_speed) % self.animation_lenght]]
		else:
			return images_dict[self.image]


	def IsOnscreen(self, screen_pos):
		sx, sy = screen_pos
		if sx < self.rect.x < sx + NB_PIX_SCREEN_X and sy < self.rect.y < sy + NB_PIX_SCREEN_Y:
			return True
		else:
			return False

	def Move(self, pressed_keys, world):
		# nx, ny = self.rect.x + int(self.speed * rand.uniform(-1, 1)), self.rect.y + int(self.speed * rand.uniform(-1, 1))
		nx, ny = self.rect.x, self.rect.y
		new_x , new_y, coll_x, coll_y = self.Collision(nx, ny, world)
		self.rect.topleft = new_x, new_y


	def Collision(self, nx, ny, world):
		i, j = 0, 0
		collision_x = False
		collision_y = False
# Collisions avec les bords
		if nx >= WORLD_WIDTH - (SCREEN_WIDTH + self.rect.w) / 2:
			nx 				= WORLD_WIDTH - (SCREEN_WIDTH + self.rect.w) / 2
			self.speeds[0] 	= 0
			collision_x 	= True
		elif nx < (SCREEN_WIDTH - self.rect.w) / 2:
			nx 				= (SCREEN_WIDTH - self.rect.w) / 2
			self.speeds[0] 	= 0
			collision_x 	= True
		if ny >= WORLD_HEIGHT - (SCREEN_HEIGHT + self.rect.h) / 2:
			ny 				= WORLD_HEIGHT - (SCREEN_HEIGHT + self.rect.h) / 2
			self.speeds[1] 	= 0
			collision_y 	= True
		elif ny < (SCREEN_HEIGHT - self.rect.h) / 2:
			ny				= (SCREEN_HEIGHT - self.rect.h) / 2
			self.speeds[1] 	= 0
			collision_y 	= True

#Collisions avec le terrain
####1 option works but might not be most efficient. Look at all cells in a 10x10 square around perso and check collision

		perso_l, perso_c = world.world_map.GetCellCoordinates(self.rect.topleft)

		obstacles = []
		for i in range(-5, 5):
			for j in range (-5, 5):
				if world.world_map.GetCellFromCoordinates((perso_l + i, perso_c + j)).collide:
					obstacles.append(world.world_map.GetCellRectFromCoordinates((perso_l + i, perso_c + j)))


		for i in obstacles:
			if   i.left - self.rect.w <= nx <= i.right and i.top - self.rect.h < self.rect.y < i.bottom and self.rect.x <= i.left - self.rect.w:#Going right, colliding with left wall
				#print("right")
				nx				= i.left - self.rect.w;
				self.speeds[0] 	= 0;
				collision_x		= True;
			elif i.left - self.rect.w <= nx <= i.right and i.top - self.rect.h < self.rect.y < i.bottom and self.rect.x >= i.right:#Going left, colliding with right wall
				#print("left")
				nx				= i.right;
				self.speeds[0] 	= 0;
				collision_x		= True;

			if   i.left - self.rect.w < self.rect.x < i.right and i.top - self.rect.h <= ny <= i.bottom and self.rect.y <= i.top - self.rect.h:#Going down, colliding with top wall
				#print("down")
				ny				= i.top - self.rect.h;
				self.speeds[1] 	= 0;
				collision_y		= True;
			elif i.left - self.rect.w < self.rect.x < i.right and i.top - self.rect.h <= ny <= i.bottom and self.rect.y >= i.bottom:#Going up, colliding with bottom wall
				#print("up")
				ny				= i.bottom;
				self.speeds[1] 	= 0;
				collision_y		= True;


###################################################################################################################
####2 option: might be more efficient, but doesn't work yet. Should check all positions along the line of mouvement. Pixel after pixel, x then y but not together
		# dx = nx - self.rect.x
		# dy = ny - self.rect.y
		# i, ix, iy = 0, 0, 0
		# hypo = (dx**2 + dy**2)**.5
		# nb_checks = dx + dy
		#
		# if(hypo):
		#
		# 	dix, diy = float(dx / ((dx**2 + dy**2)**.5)), float(dy / ((dx**2 + dy**2)**.5))
		#
		# 	while i <= nb_checks:
		# 	#while i <= nb_checks > 0 and not (collision_x and collision_y):
		# 		#print(nb_checks, ix, iy)
		# 		#print(dx, dy, int(ix * dx / nb_checks), int(ix * dy / nb_checks))
		#
		# 		if not collision_x and ix < abs(dx):
		# 			tmp_rect = pygame.Rect(self.rect.left + int(m.copysign(ix + dix, dx)), self.rect.top + int(m.copysign(iy, dy)), self.rect.w, self.rect.h)
		#
		# 			angles_rect = [	world.world_map.GetCellRectFromPosition(tmp_rect.topright),
		# 							world.world_map.GetCellRectFromPosition(tmp_rect.topleft),
		# 							world.world_map.GetCellRectFromPosition(tmp_rect.bottomright),
		# 							world.world_map.GetCellRectFromPosition(tmp_rect.bottomleft)]
		#
		# 			angles_rect = [a_r for a_r in angles_rect if world.world_map.GetCellFromPosition(a_r.center).collide]
		# 			#print(dx, dy, int(ix * dx / nb_checks), int(ix * dy / nb_checks), len(angles_rect))
		#
		# 			for cell in angles_rect:
		# 				#if tmp_rect.colliderect(cell):
		# 					#if dx > 0: # Moving right; Hit the left side of the wall
		# 						#print("right")
		# 						#nx = cell.left - self.rect.w
		# 						#self.speeds[0] 	= 0
		# 						#self.forces[0]	= 0
		# 						#collision_x 	= True
		# 					#elif dx < 0: # Moving left; Hit the right side of the wall
		# 						#print("left")
		# 						#nx = cell.right
		# 						#self.speeds[0] 	= 0
		# 						#self.forces[0]	= 0
		# 						#collision_x 	= True
		# 				if   cell.left - self.rect.w <= nx <= cell.right and cell.top - self.rect.h < self.rect.y < cell.bottom and self.rect.x <= cell.left - self.rect.w:#Going right, colliding with left wall
		# 					print("right")
		# 					nx				= cell.left - self.rect.w;
		# 					self.speeds[0] 	= 0;
		# 					self.forces[0]	= 0;
		# 					collision_x		= True;
		# 				elif cell.left - self.rect.w <= nx <= cell.right and cell.top - self.rect.h < self.rect.y < cell.bottom and self.rect.x >= cell.right:#Going left, colliding with right wall
		# 					print("left")
		# 					nx				= cell.right;
		# 					self.speeds[0] 	= 0;
		# 					self.forces[0]	= 0;
		# 					collision_x		= True;
		#
		# 			if(not collision_x): ix += dix
		#
		# 		if not collision_y and iy < abs(dy):
		# 			tmp_rect = pygame.Rect(self.rect.left + int(m.copysign(ix, dx)), self.rect.top + int(m.copysign(iy + diy, dy)), self.rect.w, self.rect.h)
		#
		# 			angles_rect = [world.world_map.GetCellRectFromPosition(tmp_rect.topright), world.world_map.GetCellRectFromPosition(tmp_rect.topleft), world.world_map.GetCellRectFromPosition(tmp_rect.bottomright), world.world_map.GetCellRectFromPosition(tmp_rect.bottomleft)]
		#
		# 			angles_rect = [a_r for a_r in angles_rect if world.world_map.GetCellFromPosition(a_r.center).collide]
		# 			for cell in angles_rect:
		# 				#if tmp_rect.colliderect(cell):
		# 					#if dy > 0: # Moving down; Hit the top side of the wall
		# 						#print("down")
		# 						#ny = cell.top - self.rect.h
		# 						#self.speeds[1] 	= 0
		# 						#self.forces[1]	= 0
		# 						#collision_y 	= True
		# 						#if self.jumps < self.max_jumps: self.jumps += 1
		# 					#elif dy < 0: # Moving up; Hit the bottom side of the wall
		# 						#print("up")
		# 						#ny = cell.bottom
		# 						#self.speeds[1] 	= 0
		# 						#self.forces[1]	= 0
		# 						#collision_y 	= True
		# 				if   cell.left - self.rect.w < self.rect.x < cell.right and cell.top - self.rect.h <= ny <= cell.bottom and self.rect.y <= cell.top - self.rect.h:#Going down, colliding with top wall
		# 					print("down")
		# 					ny				= cell.top - self.rect.h;
		# 					self.speeds[1] 	= 0;
		# 					self.forces[1]	= 0;
		# 					collision_y		= True;
		# 					if self.jumps < self.max_jumps: self.jumps += 1
		# 				elif cell.left - self.rect.w < self.rect.x < cell.right and cell.top - self.rect.h <= ny <= cell.bottom and self.rect.y >= cell.bottom:#Going up, colliding with bottom wall
		# 					print("up")
		# 					ny				= cell.bottom;
		# 					self.speeds[1] 	= 0;
		# 					self.forces[1]	= 0;
		# 					collision_y		= True;
		#
		# 			if(not collision_y): iy += diy
		#
		# 		i += 1 #i, ix, iy garanteed to be <= nb_checks

		return nx, ny, collision_x, collision_y

	def GetScreenPosition(self):
		"""Return the position of the screen origin (upper left corner) in world coordinates from perso position"""
		return (int(self.rect.x - (SCREEN_WIDTH - self.rect.w)/2), int(self.rect.y - (SCREEN_HEIGHT - self.rect.h)/2))


	def Display(self, fenetre, pos):
		"""Display the character on the screen at the given screen position"""
		fenetre.blit(self.GetImage(), pos)
		if self.speaking:
			px, py = pos
			for i, s in enumerate(self.speech):
				text_pos = px, py - (len(self.speech) - i) * font.get_linesize() - 10
				fenetre.blit(s, text_pos)





class Perso(Character):
	def __init__(self):
		Character.__init__(self, "adventurer", pos=(50 * CELL_WIDTH, 50 * CELL_HEIGHT))
		self.speed			= 10
		self.speeds			= [0, 0] #speed [east+/west-, up+/down-]
		self.direction		= -1 #-1: not moving, 0: south, 1: east, 2:north, 3:west
		self.images_folder	= "data/images/characters/perso/"
		self.image			= "I_PERSO_S_1"
		self.animation_lenght= 2
		self.animation_speed = 0.5
		self.frame_counter = 0
		self.images_list	= [	["I_PERSO_S_1", "I_PERSO_S_2"],
								["I_PERSO_E_1", "I_PERSO_E_2"],
								["I_PERSO_W_1", "I_PERSO_W_2"],
								["I_PERSO_N_1", "I_PERSO_N_2"]]

		self.position_on_screen = ((NB_PIX_SCREEN_X - self.rect.w) / 2, (NB_PIX_SCREEN_Y - self.rect.h) / 2)

		self.inventory.AddItem(Sword("base_sword", 10, 10, 1))

	def Move(self, pressed_keys, world):
		self.CalculateSpeedFromExternalEvents(pressed_keys)
		nx, ny = self.rect.x + int(self.speeds[0]), self.rect.y + int(self.speeds[1])
		new_x , new_y, coll_x, coll_y = self.Collision(nx, ny, world)
		self.rect.topleft = new_x, new_y


	def Display(self, fenetre):
		"""Always display perso on screen center"""

		fenetre.blit(self.GetImage(), self.position_on_screen)

		line = int(self.rect.x / CELL_WIDTH)
		col  = int(self.rect.y / CELL_HEIGHT)

		text_l		= font.render("l: "		+ str(line), True, (0,0,0), None)
		text_c		= font.render("c: "		+ str(col), True, (0,0,0), None)
		text_dir	= font.render("dir: "	+ str(self.direction), True, (0,0,0), None)
		fenetre.blit(text_l, 	(0, 0))
		fenetre.blit(text_c, 	(0, font.get_linesize()))
		fenetre.blit(text_dir, 	(0, 2*font.get_linesize()))

class PNG(Character):
	def __init__(self, name = "default", pos=(0,0)):
		Character.__init__(self, name, pos)
		self.speed			= 10
