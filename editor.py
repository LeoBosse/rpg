
from header import *
#from items import *
from perso import *
from carte import *
from world import *
#from mob import *


class Editor:

	def __init__(self):
		self.continuer 	= 1

		self.nb_lines	= 1000
		self.nb_columns	= 1000

		self.tab = []
		for i in xrange(self.nb_lines):
			self.tab.append([Cell("ground") for j in xrange(self.nb_columns)])



	def Edit(self, fenetre):
		print("editing")

		while self.continuer:
			self.Display(fenetre, (0,0))
			pygame.display.flip()

			self.GetExternalEvents()




	def Load(self, file_name):
		with open(file_name, 'rb') as file:
			 depickler = pickle.Unpickler(file)
			 self.tab = depickler.load()

	def Save(self, file_name):
		with open(file_name, 'wb') as file:
			 pickler = pickle.Pickler(file)
			 pickler.dump(self.tab)

	def GetCellFromCoordinates(self, (w_l, w_c)):
		"""Get Cell object corresponding to a world coordinates (w_line, w_col)"""
		return self.tab[w_l][w_c]

	def GetCellCoordinates(self, (w_x, w_y)):
		"""Get Cell corrdinates (line and column) corresponding to a world coordinates (w_x, w_y)"""
		line = int(w_x / CELL_WIDTH)
		col  = int(w_y / CELL_HEIGHT)
		return (line, col)

	def Display(self, fenetre, (screen_x, screen_y)):
		"""Display the world_map given the world position of the upper left corner of the screen"""

		fenetre.fill((0,0,255))

		cells_origin_l, cells_origin_c 	= self.GetCellCoordinates((screen_x, screen_y)) 				#line, col of origin cell
		display_origin_x, display_origin_y = -(screen_x % CELL_WIDTH), -(screen_y % CELL_HEIGHT)		#position of origin cell in screen coordinates

		for l in range(NB_CELLS_SCREEN_X / 2):
			for c in range(NB_CELLS_SCREEN_Y / 2):
				cell = self.GetCellFromCoordinates((cells_origin_l + l, cells_origin_c + c))

				fenetre.blit(cell.GetImage(), (display_origin_x + l * CELL_WIDTH, display_origin_y + c * CELL_HEIGHT));
				#fenetre.blit(cell.GetImage(), (display_origin_x + l * CELL_WIDTH, display_origin_y + c * CELL_HEIGHT));



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
