#!/usr/bin/python3.5
# -*-coding:utf-8 -*
#
# from __future__ import division
#
# # from header import *
# # from items import *
# # from perso import *
# # from carte import *
# # from world import *
# # #from mob import *
# # from game import *
# # from editor import *
#
# import os as os
# import sys as sys
# import pygame as pygame
# from pygame.locals import *
#
# import math as m
# import time as time
# import random as rand
#
# import pickle
from classes.header import *
from classes.items import *
from classes.perso import *
from classes.carte import *
from classes.world import *
from classes.game import *
#from mob import *
from classes.editor import *


def Main():

	font=pygame.font.SysFont(pygame.font.get_default_font(), 25)

	fenetre = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption("RPG")

	text_titre="WELCOME!"
	text_game1="GAME 1 (press a)"
	text_game2="GAME 2 (press b)"
	text_game3="GAME 3 (press c)"
	text_edit="Edit (press e)"

	surf_titre=font.render(text_titre, True, (255,255,255), None)
	s_titre=font.size(text_titre)
	surf_game1=font.render(text_game1, True, (255, 255, 255), None)
	s_game1=font.size(text_game1)
	surf_game2=font.render(text_game2, True, (255, 255, 255), None)
	s_game2=font.size(text_game2)
	surf_game3=font.render(text_game3, True, (255, 255, 255), None)
	s_game3=font.size(text_game3)
	surf_edit=font.render(text_edit, True, (255, 255, 255), None)
	s_edit=font.size(text_edit)
	continuer_fenetre=True

	while continuer_fenetre:
		fenetre.blit(surf_titre, ((SCREEN_WIDTH-s_titre[0])/2, 100))
		fenetre.blit(surf_game1, ((SCREEN_WIDTH-s_game1[0])/2, 100+font.get_linesize()))
		fenetre.blit(surf_game2, ((SCREEN_WIDTH-s_game2[0])/2, 100+2*font.get_linesize()))
		fenetre.blit(surf_game3, ((SCREEN_WIDTH-s_game3[0])/2, 100+3*font.get_linesize()))
		fenetre.blit(surf_edit , ((SCREEN_WIDTH-s_edit[0])/2 , 100+5*font.get_linesize()))
		pygame.display.flip()

		continuer = 1
		wait_event = True
		play = False
		edit = False
		while wait_event:
			for event in pygame.event.get():
				if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
					continuer_fenetre=False
					wait_event=False
				elif event.type==KEYDOWN:
					if event.key==K_1 or event.key==K_a:
						game_number=1
						wait_event=False
						play=True
					elif event.key==K_2 or event.key==K_b:
						game_number=2
						wait_event=False
						play=True
					elif event.key==K_3 or event.key==K_c:
						game_number=3
						wait_event=False
						play=True
					elif event.key==K_0 or event.key==K_e:
						edit = True
						wait_event=False

		if play:
			try:
				with open(PATH + "/save/save_" + str(game_number), 'rb') as file:
					depickler = pickle.Unpickler(file)
					game = depickler.load()
					print("Game loaded")
			except:
				game = Game(game_number)
				print("Game created")

			game.Play(fenetre)

			
		if edit:
			try:
				with open(PATH + "/save/edit", 'rb') as file:
					depickler = pickle.Unpickler(file)
					edit = depickler.load()
					print("Editor loaded")
			except:
				edit = Editor()
				print("Editor created")

			edit.Edit(fenetre)

	pygame.quit()



if __name__ == "__main__":
	Main()
