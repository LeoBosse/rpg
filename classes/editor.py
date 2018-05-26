#!/usr/bin/python3.5
# -*-coding:utf-8 -*
#
from classes.header import *
# from classes.items import *
# from classes.perso import *
from classes.carte import *
# from classes.world import *
# from classes.game import *
#from mob import *


class Editor:

	def __init__(self):
		self.continuer 	= 1

		self.file_name = PATH + "/save/edit"

		self.nb_lines	= NB_CELLS_WORLD_X
		self.nb_columns	= NB_CELLS_WORLD_Y

		self.display_map_ratio = 0.9

		self.Load(self.file_name)


		self.selected_cell_index = 0
		self.selected_cell = Cell(cells_list[self.selected_cell_index])


		self.screen_position = [0, 0]
		self.speed = 50
		self.pressed_keys = {	"north": 	False,
								"south":	False,
								"east":		False,
								"west":		False
								}


		self.mouse_down = False

	def Edit(self, fenetre):
		while self.continuer:
			self.Display(fenetre, self.screen_position)
			pygame.display.flip()

			self.GetExternalEvents()
			self.Move()


	def Move(self):
		if self.pressed_keys["east"] and not self.pressed_keys["west"]:
			if self.screen_position[0] + self.speed <= WORLD_WIDTH - NB_CELLS_SCREEN_X * CELL_WIDTH:
				self.screen_position[0] += self.speed
		elif self.pressed_keys["west"] and not self.pressed_keys["east"]:
			if self.screen_position[0] + self.speed >= 0:
				self.screen_position[0] -= self.speed

		if self.pressed_keys["south"] and not self.pressed_keys["north"]:
			if self.screen_position[1] + self.speed <= WORLD_HEIGHT - NB_CELLS_SCREEN_Y * CELL_HEIGHT:
				self.screen_position[1] += self.speed
		elif self.pressed_keys["north"] and not self.pressed_keys["south"]:
			if self.screen_position[1] + self.speed >= 0:
				self.screen_position[1] -= self.speed



	def Load(self, file_name):
		print("Loading...")
		with open(file_name, 'rb') as file:
			 depickler = pickle.Unpickler(file)
			 self.name_tab = depickler.load()

		self.tab = []
		for i in range(self.nb_lines):
			self.tab.append([])
			for j in range(self.nb_columns):
				self.tab[i].append(Cell(self.name_tab[i][j]))
		print("Loaded")

	def Save(self, file_name):
		print("Saving...")
		self.name_tab = []
		for i in range(self.nb_lines):
			self.name_tab.append([])
			for j in range(self.nb_columns):
				self.name_tab[i].append(self.tab[i][j].name)
		with open(file_name, 'wb') as file:
			 pickler = pickle.Pickler(file)
			 pickler.dump(self.name_tab)
		print("Saved")


	def GetCellFromCoordinates(self, w_coor):
		"""Get Cell object corresponding to a world coordinates (w_line, w_col)"""
		w_l, w_c = w_coor
		return self.tab[w_l][w_c]

	def GetCellCoordinates(self, w_pos):
		"""Get Cell corrdinates (line and column) corresponding to a world coordinates (w_x, w_y)"""
		w_x, w_y = w_pos
		line = int(w_x / CELL_WIDTH)
		col  = int(w_y / CELL_HEIGHT)
		return (line, col)

	def Display(self, fenetre, screen_pos):
		"""Display the world_map given the world position of the upper left corner of the screen"""
		screen_x, screen_y = screen_pos
		fenetre.fill((0,0,255))

		cells_origin_l, cells_origin_c 	= self.GetCellCoordinates((screen_x, screen_y)) 				#line, col of origin cell
		display_origin_x, display_origin_y = -(screen_x % CELL_WIDTH), -(screen_y % CELL_HEIGHT)		#position of origin cell in screen coordinates

		for l in range(1 + int(NB_CELLS_SCREEN_X * self.display_map_ratio)):
			for c in range(NB_CELLS_SCREEN_Y):
				cell = self.GetCellFromCoordinates((cells_origin_l + l, cells_origin_c + c))
				fenetre.blit(cell.GetImage(), (display_origin_x + l * CELL_WIDTH, display_origin_y + c * CELL_HEIGHT));
				# pygame.draw.rect(fenetre, (255,0,0), (display_origin_x + l * CELL_WIDTH, display_origin_y + c * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT), 1)
				pygame.draw.line(fenetre, (255,0,0), (display_origin_x + l * CELL_WIDTH, 0),(display_origin_x + l * CELL_WIDTH, NB_PIX_SCREEN_Y))
				pygame.draw.line(fenetre, (255,0,0), (0, display_origin_y + c * CELL_HEIGHT),(NB_PIX_SCREEN_X, display_origin_y + c * CELL_HEIGHT))

				#fenetre.blit(cell.GetImage(), (display_origin_x + l * CELL_WIDTH, display_origin_y + c * CELL_HEIGHT));

		pygame.draw.rect(fenetre, (0,0,0), (NB_PIX_SCREEN_X * self.display_map_ratio, 0, NB_PIX_SCREEN_X, NB_PIX_SCREEN_Y))
		for i, c in enumerate(cells_list):
			fenetre.blit(Cell(c).GetImage(), ((NB_PIX_SCREEN_X * self.display_map_ratio + int(i / NB_CELLS_SCREEN_Y)), i * CELL_HEIGHT));
		pygame.draw.rect(fenetre, (255,0,0), ((NB_PIX_SCREEN_X * self.display_map_ratio + int(self.selected_cell_index / NB_CELLS_SCREEN_Y)), self.selected_cell_index * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT), 2);

	def GetExternalEvents(self):
		for event in pygame.event.get():
			if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
				self.continuer=0

			elif event.type==MOUSEBUTTONDOWN and event.button==1:
				self.ManageMouseCLIC(event.pos, "down")
			elif  event.type==MOUSEBUTTONUP and event.button==1:
				self.ManageMouseCLIC(event.pos, "up")

			elif event.type==KEYDOWN:
				if event.key == K_UP or event.key == K_z:
					self.pressed_keys["north"] = True
				elif event.key == K_DOWN or event.key == K_s:
					if self.pressed_CTRL:
						self.Save(self.file_name)
					else:
						self.pressed_keys["south"] = True
				elif event.key==K_LEFT or event.key == K_q:
					self.pressed_keys["west"] = True
				elif event.key==K_RIGHT or event.key == K_d:
					self.pressed_keys["east"] = True
				elif event.key==K_LCTRL or event.key==K_RCTRL:
					self.pressed_CTRL = True
				elif event.key==K_l:
					self.Load(self.file_name)

			elif event.type==KEYUP:
				if event.key == K_UP or event.key == K_z:
					self.pressed_keys["north"] = False
				elif event.key == K_DOWN or event.key == K_s:
					self.pressed_keys["south"] = False
				elif event.key==K_LEFT or event.key == K_q:
					self.pressed_keys["west"] = False
				elif event.key==K_RIGHT or event.key == K_d:
					self.pressed_keys["east"] = False
				elif event.key==K_LCTRL or K_RCTRL:
					self.pressed_CTRL = False

	def ManageMouseCLIC(self, pos, type):
		x, y = pos
		if type == "down" and x > NB_PIX_SCREEN_X * self.display_map_ratio:
			n = int((x - NB_PIX_SCREEN_X * self.display_map_ratio) / CELL_WIDTH) * int(NB_PIX_SCREEN_Y / CELL_HEIGHT) + int(y / CELL_HEIGHT)
			if n < len(cells_list):
				self.selected_cell_index = n
				self.selected_cell = Cell(cells_list[self.selected_cell_index])

		elif type == "down" and x < NB_PIX_SCREEN_X * self.display_map_ratio:
			self.mouse_down = True
			self.mouse_start_pos = (x, y)

		elif self.mouse_down and type == "up" and x < NB_PIX_SCREEN_X * self.display_map_ratio:
			self.mouse_down = False
			w1, c1 = self.GetCellCoordinates((self.mouse_start_pos[0] + self.screen_position[0], self.mouse_start_pos[1] + self.screen_position[1]))
			w2, c2 = self.GetCellCoordinates((x + self.screen_position[0], y + self.screen_position[1]))

			for w in range(min(w1, w2), max(w1, w2) + 1):
				for c in range(min(c1, c2), max(c1, c2) + 1):
					self.tab[w][c] = self.selected_cell

		elif self.mouse_down and type == "up":
			self.mouse_down = False
