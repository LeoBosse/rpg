#!/usr/bin/python3.5
# -*-coding:utf-8 -*
# #
from classes.header import *
from classes.items import *
# from classes.perso import *
# from classes.world import *
# from classes.game import *
# #from mob import *
# from classes.editor import *

class World_Map:
	def __init__(self, world):
		self.time 			= 0

		#All elements inherited from world instance
		self.nb_lines	= world.nb_lines
		self.nb_columns	= world.nb_columns


		self.tab = []
		# for i in range(self.nb_lines):
		# 	self.tab.append([Cell("ground") for j in range(self.nb_columns)])
		#
		# for i in range(self.nb_lines):
		# 	for j in range(self.nb_columns):
		# 		if(i%3==0 and j%3==0):
		# 			self.tab[i][j] = Cell("tree")

		self.Load("save/edit")


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


### World POSITIONS is the cell id expressed in PIXELS (0, 0) = top left corner
### World COORDINATES is the cell id expressed in CELL NUMBERS (0, 0) = top left corner
### cell (0, 0) has position (0, 0) (up, middle)

	def GetCellFromPosition(self, w_pos):
		"""Get Cell object corresponding to a world position (w_x, w_y)"""
		w_x, w_y = w_pos
		line, col = self.GetCellCoordinates((w_x, w_y))
		if 0 < line < len(self.tab) and 0 < col < len(self.tab[line]):
			return self.tab[line][col]
		else:
			return Cell("black")

	def GetCellFromCoordinates(self, w_coor):
		"""Get Cell object corresponding to a world coordinates (w_line, w_col)"""
		w_l, w_c = w_coor
		if 0 < w_l < len(self.tab) and 0 < w_c < len(self.tab[w_l]):
			return self.tab[w_l][w_c]
		else:
			return Cell("black")

	def GetCellCoordinates(self, w_pos):
		"""Get Cell corrdinates (line and column) corresponding to a world coordinates (w_x, w_y)"""
		w_x, w_y = w_pos
		line = int(w_x / CELL_WIDTH)
		col  = int(w_y / CELL_HEIGHT)
		return (line, col)

	def GetCellPosition(self, w_coor):
		"""Get Cell position of lower left corner (w_x, w_y) from world coordinates (w_l, w_c)"""
		w_l, w_c = w_coor
		x = w_l * CELL_WIDTH
		y = w_c * CELL_HEIGHT
		return (x, y)

	def GetCellRectFromCoordinates(self, w_coor):
		"""Get Cell pygame.Rect from world coordinates (w_l, w_c)"""
		w_l, w_c = w_coor
		x, y = self.GetCellPosition((w_l, w_c))
		return pygame.Rect(x, y, CELL_WIDTH, CELL_HEIGHT)

	def GetCellRectFromPosition(self, w_pos):
		"""Get the Cell pygame.Rect containing world position (w_x, w_y)"""
		return self.GetCellRectFromCoordinates(self.GetCellCoordinates(w_pos))

	def GetLineCoordinatesFromPosition(self, w_x):
		"""Return the line coordinate from a pixel position. !!! Can be different from its place in self.lines[] !!! -> Use _GetLignIndexInList() for that."""
		return int(w_x / CELL_WIDTH)


	def Display(self, fenetre, screen_pos, perso):
		"""Display the world_map given the world position of the upper left corner of the screen"""
		screen_x, screen_y = screen_pos
		fenetre.fill((0,0,255))

		cells_origin_l, cells_origin_c 	= self.GetCellCoordinates((screen_x, screen_y)) 				#line, col of origin cell
		display_origin_x, display_origin_y = -(screen_x % CELL_WIDTH), -(screen_y % CELL_HEIGHT)		#position of origin cell in screen coordinates

		for l in range(NB_CELLS_SCREEN_X + 1):
			for c in range(NB_CELLS_SCREEN_Y + 1):
				cell = self.GetCellFromCoordinates((cells_origin_l + l, cells_origin_c + c))

				cell.Display(fenetre, (display_origin_x + l * CELL_WIDTH, display_origin_y + c * CELL_HEIGHT))
				# fenetre.blit(cell.GetImage(self.CellVisibility((cells_origin_l + l, cells_origin_c + c), perso)), (display_origin_x + l * CELL_WIDTH, display_origin_y + c * CELL_HEIGHT));

					#text_cell_l = font2.render(str(cells_origin_l + l), True, (255,0,0), None)
					#text_cell_c = font2.render(str(cells_origin_c - c), True, (255,0,0), None)
					#fenetre.blit(text_cell_l, (display_origin_x + l * CELL_WIDTH, display_origin_y + c * CELL_HEIGHT))
					#fenetre.blit(text_cell_c, (display_origin_x + l * CELL_WIDTH, display_origin_y + c * CELL_HEIGHT + font2.get_linesize()))
			#for l in range(NB_CELLS_SCREEN_X + 1):
				#pygame.draw.line(fenetre, (255, 0, 0), (display_origin_x, display_origin_y + l * CELL_HEIGHT), (SCREEN_WIDTH, display_origin_y + l * CELL_HEIGHT))
				#pygame.draw.line(fenetre, (255, 0, 0), (display_origin_x + l * CELL_WIDTH, display_origin_y), (display_origin_x + l * CELL_WIDTH, SCREEN_HEIGHT))


class Cell:
	def __init__(self, cell_type):
		self.name			= cell_type
		self.width 			= CELL_WIDTH
		self.height 		= CELL_HEIGHT
		self.friction 		= -5.

		self.inventory = Inventory()

		if self.name == "grass":
			self.image 			= I_GRASS
			self.image_shadow 	= I_GRASS
			self.collide		= False

		elif self.name == "tree":
			self.image 			= I_TREE
			self.image_shadow 	= I_TREE
			self.collide		= True

		elif self.name == "water":
			self.image 			= I_WATER
			self.image_shadow 	= I_WATER
			self.collide		= True

		elif self.name == "rock":
			self.image 			= I_ROCK
			self.image_shadow 	= I_ROCK
			self.collide		= True

		else:
			self.image 			= I_BLACK
			self.image_shadow 	= I_BLACK
			self.collide		= True

	def Display(self, fenetre, pos):
		x, y = pos
		fenetre.blit(self.GetImage(True), (x, y));
		self.inventory.Display(fenetre, (x, y))

	def GetImage(self, visible = True):
		if visible:
			return self.image
		else:
			return self.image_shadow
