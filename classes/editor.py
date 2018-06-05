#!/usr/bin/python3.5
# -*-coding:utf-8 -*
#
from classes.header import *
from classes.items import *
from classes.perso import *
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
		self.type_button_height = 50
		self.world_cell_button_rect = pygame.Rect(int(NB_PIX_SCREEN_X * self.display_map_ratio), 0, (NB_PIX_SCREEN_X * (1 - self.display_map_ratio)) / 3, self.type_button_height)
		self.items_button_rect = pygame.Rect(self.world_cell_button_rect.right, 0, self.world_cell_button_rect.w, self.world_cell_button_rect.h)
		self.PNGs_button_rect = pygame.Rect(self.items_button_rect.right, 0, self.world_cell_button_rect.w, self.world_cell_button_rect.h)

		self.world_cells_list = [Cell("grass"), Cell("tree"), Cell("water"), Cell("rock"),Cell("black"), Cell("wood"), Cell("sand"), Cell("planck")]
		self.items_cells_list = [Sword("basic sword", 1, 10, 10)]
		self.PNGs_cells_list = [PNG()]


		self.list_type = "world"
		self.cell_list = self.world_cells_list

		self.PNGs = []

		# self.pressed_CTRL = False

		self.diplayed_cells_list_rect = pygame.Rect(int(NB_PIX_SCREEN_X * self.display_map_ratio), self.world_cell_button_rect.h, NB_PIX_SCREEN_X * (1 - self.display_map_ratio), NB_PIX_SCREEN_Y)



		self.tab = []
		for i in range(self.nb_lines):
			self.tab.append([])
			for j in range(self.nb_columns):
				self.tab[i].append(Cell("grass"))


		self.selected_cell_index = 0
		self.selected_cell = self.world_cells_list[self.selected_cell_index]





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

	def AskQuestion(self, question):
		answer = ""
		text_question = font.render(question, True, (0,0,0), None)
		w, h = font.size(question)
		h += font.get_linesize()

		wait_answer = True
		while wait_answer:
			w = max(font.size(question)[0], font.size(answer)[0])
			display_rect = pygame.Rect(int((NB_PIX_SCREEN_X - w) / 2), int((NB_PIX_SCREEN_Y - h) / 2), w, h)
			pygame.draw.rect(fenetre, (255,255,255), display_rect)
			fenetre.blit(text_question, display_rect)

			text_answer = font.render(answer, True, (0,0,0), None)
			fenetre.blit(text_answer, display_rect.move(0, font.get_linesize()))

			pygame.display.flip()

			for event in pygame.event.get():
				if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE) or (event.type==KEYDOWN and event.key==K_RETURN):
					wait_answer = False
				elif event.type==KEYDOWN and (65 <= event.key <= 90 or 97 <= event.key <= 122 or 48 <= event.key <= 57):
					answer += pygame.key.name(event.key)
					print(answer)
				elif event.type==KEYDOWN and event.key == K_BACKSPACE:
					answer = answer[:-1]

		return answer



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



	# def Load(self, file_name):
	# 	print("Loading...")
	# 	with open(file_name, 'rb') as file:
	# 		depickler = pickle.Unpickler(file)
	# 		self = depickler.load()
	#
	# 	# self.tab = []
	# 	# for i in range(self.nb_lines):
	# 	# 	self.tab.append([])
	# 	# 	for j in range(self.nb_columns):
	# 	# 		try:
	# 	# 			self.tab[i].append(Cell(self.loaded_tab[i][j]))
	# 	# 		except:
	# 	# 			self.tab[i].append(Cell("grass"))
	# 	print("Loaded")

	def Save(self, file_name):
		print("Saving...")
		# self.saved_tab = []
		# for i in range(self.nb_lines):
		# 	self.saved_tab.append([])
		# 	for j in range(self.nb_columns):
		# 		self.saved_tab[i].append(self.tab[i][j].GetSavedAttribute())
		with open(file_name, 'wb') as file:
			 pickler = pickle.Pickler(file)
			 pickler.dump(self)
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

		for l in range(1 + int(self.diplayed_cells_list_rect.x / CELL_WIDTH)):
			for c in range(NB_CELLS_SCREEN_Y + 1):
				cell = self.GetCellFromCoordinates((cells_origin_l + l, cells_origin_c + c))
				# fenetre.blit(cell.GetImage(), (display_origin_x + l * CELL_WIDTH, display_origin_y + c * CELL_HEIGHT));
				cell.Display(fenetre, (display_origin_x + l * CELL_WIDTH, display_origin_y + c * CELL_HEIGHT))
				# pygame.draw.rect(fenetre, (255,0,0), (display_origin_x + l * CELL_WIDTH, display_origin_y + c * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT), 1)
				pygame.draw.line(fenetre, (255,0,0), (display_origin_x + l * CELL_WIDTH, 0),(display_origin_x + l * CELL_WIDTH, NB_PIX_SCREEN_Y))
				pygame.draw.line(fenetre, (255,0,0), (0, display_origin_y + c * CELL_HEIGHT),(NB_PIX_SCREEN_X, display_origin_y + c * CELL_HEIGHT))

				#fenetre.blit(cell.GetImage(), (display_origin_x + l * CELL_WIDTH, display_origin_y + c * CELL_HEIGHT));

		for i, png in enumerate(self.PNGs):
			png.Display(fenetre, png.GetPositionOnScreen(self.screen_position))

		#Display the cell coordinates
		for l in range(1 + int(self.diplayed_cells_list_rect.x / CELL_WIDTH)):
			text	= font2.render(str(cells_origin_l + l), True, (0,0,0), None)
			fenetre.blit(text, 	(display_origin_x + l * CELL_WIDTH, 0))
		for c in range(NB_CELLS_SCREEN_Y + 1):
			text	= font2.render(str(cells_origin_c + c), True, (0,0,0), None)
			fenetre.blit(text, 	(0, display_origin_y + c * CELL_HEIGHT))

		#Display the cell type button in the right continuer_fenetre
		pygame.draw.rect(fenetre, (255,0,0), self.world_cell_button_rect)
		text	= font.render("World", True, (0,0,0), None)
		fenetre.blit(text, 	self.world_cell_button_rect)
		pygame.draw.rect(fenetre, (0,255,0), self.items_button_rect)
		text	= font.render("Items", True, (0,0,0), None)
		fenetre.blit(text, 	self.items_button_rect)
		pygame.draw.rect(fenetre, (0,0,255), self.PNGs_button_rect)
		text	= font.render("PNGs", True, (0,0,0), None)
		fenetre.blit(text, 	self.PNGs_button_rect)

		#Display the cell list on the right of the screen
		pygame.draw.rect(fenetre, (0,0,0), self.diplayed_cells_list_rect)
		for i, c in enumerate(self.cell_list):
			fenetre.blit(c.GetImage(), (self.diplayed_cells_list_rect.x + int((i * CELL_HEIGHT) / self.diplayed_cells_list_rect.h), self.diplayed_cells_list_rect.top + (i % (self.diplayed_cells_list_rect.h / CELL_HEIGHT)) * CELL_HEIGHT));

		pygame.draw.rect(fenetre, (255,0,0), (self.diplayed_cells_list_rect.x + int((self.selected_cell_index * CELL_HEIGHT) / self.diplayed_cells_list_rect.h), self.diplayed_cells_list_rect.top + (self.selected_cell_index % (self.diplayed_cells_list_rect.h / CELL_HEIGHT)) * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT), 2);

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
					if pygame.key.get_pressed()[K_LCTRL] or pygame.key.get_pressed()[K_RCTRL]:
						self.Save(self.file_name)
					else:
						self.pressed_keys["south"] = True
				elif event.key==K_LEFT or event.key == K_q:
					self.pressed_keys["west"] = True
				elif event.key==K_RIGHT or event.key == K_d:
					self.pressed_keys["east"] = True
				# elif event.key==K_LCTRL or event.key==K_RCTRL:
				# 	self.pressed_CTRL = True
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
				# elif event.key==K_LCTRL or K_RCTRL:
				# 	self.pressed_CTRL = False

	def ManageMouseCLIC(self, pos, type):
		x, y = pos
		if type == "down" and x > self.diplayed_cells_list_rect.x:
			if self.world_cell_button_rect.top < y < self.world_cell_button_rect.bottom:
				if self.world_cell_button_rect.left < x < self.world_cell_button_rect.right:
					self.list_type = "world"
					self.cell_list = self.world_cells_list
				elif self.items_button_rect.left < x < self.items_button_rect.right:
					self.list_type = "items"
					self.cell_list = self.items_cells_list
				elif self.PNGs_button_rect.left < x < self.PNGs_button_rect.right:
					self.list_type = "PNGs"
					self.cell_list = self.PNGs_cells_list

			elif y > self.diplayed_cells_list_rect.top:
				n = int((x - self.diplayed_cells_list_rect.x) / CELL_WIDTH) * int(self.diplayed_cells_list_rect.h / CELL_HEIGHT) + int((y - self.diplayed_cells_list_rect.top) / CELL_HEIGHT)
				if n < len(self.cell_list):
					self.selected_cell_index = n
					self.selected_cell = self.cell_list[self.selected_cell_index]

		elif type == "down" and x < self.diplayed_cells_list_rect.x:
			self.mouse_down = True
			self.mouse_start_pos = (x + self.screen_position[0], y + self.screen_position[1])

		elif self.mouse_down and type == "up" and x < self.diplayed_cells_list_rect.x:
			self.mouse_down = False
			w1, c1 = self.GetCellCoordinates((self.mouse_start_pos[0], self.mouse_start_pos[1]))
			w2, c2 = self.GetCellCoordinates((x + self.screen_position[0], y + self.screen_position[1]))

			if self.list_type == "world":
				for w in range(min(w1, w2), max(w1, w2) + 1):
					for c in range(min(c1, c2), max(c1, c2) + 1):
						self.tab[w][c] = self.selected_cell
			elif self.list_type == "items":
				print("Adding an item to a cell")
				self.tab[w2][c2].AddItem(self.selected_cell)
			elif self.list_type == "PNGs":
				PNG_name = self.AskQuestion("What is its name?")
				self.PNGs.append(PNG(PNG_name, (x + self.screen_position[0], y + self.screen_position[1])))



		elif self.mouse_down and type == "up":
			self.mouse_down = False
