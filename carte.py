#!/usr/bin/python
# -*-coding:utf-8 -*
##!/usr/local/bin/python3


from header import *

class World_Map:

	def __init__(self, world):
		self.time 			= 0

		#All elements inherited from world instance
		self.nb_lines	= world.nb_lines
		self.nb_columns	= world.nb_columns
		# self.biom_list 		= world.biom_list



		#Creation of the lines
		# self.mean_biom_length 	= 100
		self.tab = []
		for i in xrange(self.nb_lines):
			self.tab.append([Cell("ground") for j in xrange(self.nb_columns)])

		for i in xrange(self.nb_lines):
			for j in xrange(self.nb_columns):
				if(i%3==0 and j%3==0):
					self.tab[i][j] = Cell("tree")


	def Load(self, file_name):
		with open(file_name, 'rb') as file:
			 depickler = pickle.Unpickler(file)
			 self.tab = depickler.load()

	def Save(self, file_name):
		with open(file_name, 'wb') as file:
			 pickler = pickle.Pickler(file)
			 pickler.dump(self.tab)

### World POSITIONS is the cell id expressed in PIXELS (0, 0) = top left corner
### World COORDINATES is the cell id expressed in CELL NUMBERS (0, 0) = top left corner
### cell (0, 0) has position (0, 0) (up, middle)

	def GetCellFromPosition(self, (w_x, w_y)):
		"""Get Cell object corresponding to a world position (w_x, w_y)"""
		line, col = self.GetCellCoordinates((w_x, w_y))
		return self.tab[line][col]

	def GetCellFromCoordinates(self, (w_l, w_c)):
		"""Get Cell object corresponding to a world coordinates (w_line, w_col)"""
		return self.tab[w_l][w_c]

	def GetCellCoordinates(self, (w_x, w_y)):
		"""Get Cell corrdinates (line and column) corresponding to a world coordinates (w_x, w_y)"""
		line = int(w_x / CELL_WIDTH)
		col  = int(w_y / CELL_HEIGHT)
		return (line, col)

	def GetCellPosition(self, (w_l, w_c)):
		"""Get Cell position of lower left corner (w_x, w_y) from world coordinates (w_l, w_c)"""
		x = w_l * CELL_WIDTH
		y = w_c * CELL_HEIGHT
		return (x, y)

	def GetCellRectFromCoordinates(self, (w_l, w_c)):
		"""Get Cell pygame.Rect from world coordinates (w_l, w_c)"""
		x, y = self.GetCellPosition((w_l, w_c))
		return pygame.Rect(x, y, CELL_WIDTH, CELL_HEIGHT)

	def GetCellRectFromPosition(self, (w_x, w_y)):
		"""Get the Cell pygame.Rect containing world position (w_x, w_y)"""
		return self.GetCellRectFromCoordinates(self.GetCellCoordinates((w_x, w_y)))

	# def _GetLignIndexInList(self, line_coordinate):
	# 	"""Return the line position in the self.lines[] list from the line world coordinates (w_l)"""
	# 	result = line_coordinate - self.lines[0].coordinate
	# 	if result < 0 or result >= len(self.lines):
	# 		return False
	# 	else:
	# 		return result

	def GetLineCoordinatesFromPosition(self, w_x):
		"""Return the line coordinate from a pixel position. !!! Can be different from its place in self.lines[] !!! -> Use _GetLignIndexInList() for that."""
		return int(w_x / CELL_WIDTH)

	# def GetLineFromPosition(self, w_x):
	# 	"""Return the line number from a pixel position. !!! Can be different from its place in self.lines[] !!! -> Use _GetLignIndexInList() for that."""
	# 	return self.lines[self._GetLignIndexInList(self.GetLineCoordinatesFromPosition(w_x))]


	# def GetAltitudeFromPosition(self, w_x):
	# 	"""Return the altitude of the line from a pixel position"""
		# return self.GetLineFromPosition(w_x).GetAltitude()


	def Display(self, fenetre, (screen_x, screen_y), perso):
		"""Display the world_map given the world position of the upper left corner of the screen"""

		fenetre.fill((0,0,255))

		cells_origin_l, cells_origin_c 	= self.GetCellCoordinates((screen_x, screen_y)) 				#line, col of origin cell
		display_origin_x, display_origin_y = -(screen_x % CELL_WIDTH), -(screen_y % CELL_HEIGHT)		#position of origin cell in screen coordinates

		for l in range(NB_CELLS_SCREEN_X + 1):
			for c in range(NB_CELLS_SCREEN_Y + 1):
				cell = self.GetCellFromCoordinates((cells_origin_l + l, cells_origin_c + c))

				fenetre.blit(cell.GetImage(self.CellVisibility((cells_origin_l + l, cells_origin_c + c), perso)), (display_origin_x + l * CELL_WIDTH, display_origin_y + c * CELL_HEIGHT));
				#fenetre.blit(cell.GetImage(), (display_origin_x + l * CELL_WIDTH, display_origin_y + c * CELL_HEIGHT));
				cell = self.GetCellFromCoordinates((cells_origin_l + l, cells_origin_c + c))

					#text_cell_l = font2.render(str(cells_origin_l + l), True, (255,0,0), None)
					#text_cell_c = font2.render(str(cells_origin_c - c), True, (255,0,0), None)
					#fenetre.blit(text_cell_l, (display_origin_x + l * CELL_WIDTH, display_origin_y + c * CELL_HEIGHT))
					#fenetre.blit(text_cell_c, (display_origin_x + l * CELL_WIDTH, display_origin_y + c * CELL_HEIGHT + font2.get_linesize()))
			#for l in range(NB_CELLS_SCREEN_X + 1):
				#pygame.draw.line(fenetre, (255, 0, 0), (display_origin_x, display_origin_y + l * CELL_HEIGHT), (SCREEN_WIDTH, display_origin_y + l * CELL_HEIGHT))
				#pygame.draw.line(fenetre, (255, 0, 0), (display_origin_x + l * CELL_WIDTH, display_origin_y), (display_origin_x + l * CELL_WIDTH, SCREEN_HEIGHT))

	# def CellSurrounded(self, (w_l, w_c)):
	# 	"""	Return true if cell is not in contact with air. (or a cell where perso can go cell.transparent==False). Corners count!
	# 		Is surrounded by default. If there is a transparent cell next to it, we break the loop and result=False"""
	#
	# 	line_index = self._GetLignIndexInList(w_l)
	# 	for l in self.lines[line_index - 1:line_index + 2]: 		#Loop over the 3 lines in contact (1 before, 1 after, the line with the cell)
	# 		for c in range(w_c - 1, w_c + 2):							#Loop over the 3 altitudes that can be in contact
	# 			if self.GetCellFromCoordinates((l.coordinate, c)).transparent:		#If the neighbourg cell is transparent
	# 				return False										#	return False (it is not surrounded)
	# 	return True														#If no neighbourg cell is transparent, return True (it is surrounded)



	def CellVisibility(self, (w_l, w_c), perso):
		"""	Return True if cell is in light, visible by perso. Return False if cell is underground in shadow.
			There is no point in asking an "air" or "ground" tile since they should always be visible"""

		# if self.GetCellFromCoordinates((w_l, w_c)).name in ["ground",  "air"]:
			# return True

		#self.GetCellsInPersoVision(perso)
		#if (w_l, w_c) in self.cells_in_perso_vision:
			#return True

		#if self.CellSurrounded((w_l, w_c)):
			#return False

		#line_index = self._GetLignIndexInList(w_l)
		return True

	# def GetCellsInPersoVision(self, perso):
	# 	px, py		= perso.rect.center
	# 	pl, pc 		= self.GetCellCoordinates((px, py))
	# 	radius_max 	= perso.GetVisionRadius()
	# 	da			= 2 * m.pi * CELL_WIDTH / radius_max
	# 	dr			= CELL_WIDTH
	# 	a			= 0
	#
	# 	self.cells_in_perso_vision = []
	# 	blocked_angles = []
	#
	# 	rad = 0
	# 	r = 0
	# 	while rad < radius_max:
	# 		rad = min(r * dr, radius_max)
	# 		Na 	= 2 * m.pi * rad / CELL_WIDTH + 1
	# 		for a in [2 * m.pi * i / Na for i in range(int(Na))]:
	# 			dl, dc = self.GetCellCoordinates((int(rad* m.cos(a)), int(rad * m.sin(a))))
	# 			if self.GetCellFromCoordinates((pl + dl, pc + dc)).transparent:
	# 				dead_angle = False
	# 				it = 0
	# 				while it < len(blocked_angles) and not dead_angle:
	# 					if blocked_angles[it][0] <= a <= blocked_angles[it][1]:
	# 						dead_angle = True
	# 					it += 1
	# 				#if (pl + dl, pc + dc) in self.cells_in_perso_vision:
	# 				if not dead_angle:
	# 					self.cells_in_perso_vision.append((pl + dl, pc + dc))
	# 			else:
	# 				blocked_angles.append((a - m.pi / Na, a + m.pi / Na))
	#
	#
	# 		r += 1

		#while a * da < 2 * m.pi:
			#r = 0
			#angle_visibility = True
			#while angle_visibility and r * dr < radius_max:
				#dl, dc = self.GetCellCoordinates((int(r * dr * m.cos(a * da)), int(r * dr * m.sin(a * da))))
				#if angle_visibility and self.GetCellFromCoordinates((pl + dl, pc + dc)).transparent:
					#if (pl + dl, pc + dc) in self.cells_in_perso_vision:
						#self.cells_in_perso_vision.append((pl + dl, pc + dc))
				#else:
					#angle_visibility = False
				#r += 1
			#a += 1
		#return self.cells_in_perso_vision


#
# class Lign:
# 	def __init__(self, world_map , east_or_west = 0):
# 		"""Initialise a line east (1) or west (-1) from the seed_line (first or last line in world_map.lines[]), coordinate = 0 if len(world_map.lines[])==0"""
#
# 		if len(world_map.lines) == 0 or east_or_west == 0:
# 			self.coordinate		= 0
# 			self.altitude 		= int(NB_CELLS_WORLD_Y / 2)
# 			self.biom 			= world_map.biom_list[0]
# 			self.general_slope	= rand.gauss(0., self.biom.average_slope)
#
# 		else:
# 			seed_line = 0
# 			if east_or_west == -1 or east_or_west == "west":
# 				seed_line = world_map.lines[0]
# 				self.coordinate		= seed_line.coordinate - 1
# 			else: #add a line to the east
# 				seed_line = world_map.lines[-1]
# 				self.coordinate		= seed_line.coordinate + 1
#
# 			self.Grow(world_map, seed_line)
#
#
#
# 		self.nb_cells		= NB_CELLS_WORLD_Y
# 		self.cave_proba		= 0.05
# 		self.diamond_proba	= 0.5
# 		self.diamond_max_height = NB_CELLS_WORLD_Y/5
# 		self.water_proba	= 0.1
# 		self.pente 			= 0.6
# 		self.cave_height	= 13
#
# 		self.layers			= [(0, Cell(self.biom, "air")), (self.GetAltitude(), Cell(self.biom, "ground")), (self.GetAltitude() + 1, Cell(self.biom, "under_ground"))]
#
# 	def Grow(self, world_map, seed_line):
# 		"""Initialize the line parameter based on a seed, the biom and the world map"""
#
# 		if rand.random() < 1. / world_map.mean_biom_length: #Changing biom
# 			self.biom = world_map.biom_list[rand.randint(0, len(world_map.biom_list) - 1)]
# 		else:
# 			self.biom = seed_line.biom
#
# 		#Find altitude as function  of biom and seed_line
# 		if rand.random() > 1. / self.biom.slope_continuity and self.biom.name == seed_line.biom.name:
# 			self.general_slope 	= seed_line.general_slope
# 			self.altitude		= seed_line.altitude + self.general_slope
# 		else:
# 			self.general_slope 	= rand.gauss(0., self.biom.average_slope)
# 			self.altitude		= seed_line.altitude + self.general_slope
#
#
# 	def GetAltitude(self):
# 		"""self.altitude is a float. This function is made to reurn the corresponding int()"""
# 		return int(self.altitude)
#
# 	def GetCell(self, col):
# 		"""Return the Cell object at this position"""
# 		i = 0
# 		while i < len(self.layers) and self.layers[i][0] <= col:
# 			i += 1
# 		return self.layers[i-1][1]
#


class Cell:
	def __init__(self, cell_type):
		self.name			= cell_type
		self.width 			= CELL_WIDTH
		self.height 		= CELL_HEIGHT
		self.friction 		= -5.

		if self.name == "ground":
			self.image 			= I_GRASS
			self.image_shadow 	= I_GRASS
			self.collide		= False
			# self.transparent	= False


		elif self.name == "tree":
			self.image 			= I_TREE
			self.image_shadow 	= I_TREE
			self.collide		= True
			# self.transparent	= False


	def GetImage(self, visible = True):
		if visible:
			return self.image
		else:
			return self.image_shadow
