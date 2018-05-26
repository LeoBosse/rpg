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
#
# PATH = "/home/leo/ProgrammesPython/rpg/"
#
#
# a = pygame.init()[1]
# while a != 0:
# 	a = pygame.init()[1]
#
# font = pygame.font.SysFont(pygame.font.get_default_font(), 25)
# font2 = pygame.font.SysFont(pygame.font.get_default_font(), 20)
#
# Info = pygame.display.Info()
#
# SCREEN_HEIGHT	= Info.current_h-100
# SCREEN_WIDTH	= Info.current_w-100
#
# fenetre = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("RPG")
#
#
# CELL_WIDTH 			= 20
# CELL_HEIGHT  		= 20
#
# NB_CELLS_SCREEN_X 	= int(SCREEN_WIDTH / CELL_WIDTH + 1)
# NB_CELLS_SCREEN_Y	= int(SCREEN_HEIGHT / CELL_HEIGHT + 1)
#
# NB_CELLS_WORLD_X 	= NB_CELLS_SCREEN_X * 10
# NB_CELLS_WORLD_Y 	= NB_CELLS_SCREEN_Y * 10
#
# NB_PIX_SCREEN_X   	= NB_CELLS_SCREEN_X * CELL_WIDTH
# NB_PIX_SCREEN_Y   	= NB_CELLS_SCREEN_Y * CELL_HEIGHT
#
# WORLD_WIDTH  	= NB_CELLS_WORLD_X * CELL_WIDTH
# WORLD_HEIGHT   	= NB_CELLS_WORLD_Y * CELL_HEIGHT
#
# g_fps 			= 30		#g_fps turns per seconds
# g_turn_duration	= 1./g_fps	#duration of a turn (in seconds)
#
# cells_list = ["grass", "tree", "water", "rock", "black"]
#
# I_GRASS			= pygame.image.load("images/grass.bmp").convert()
# I_TREE			= pygame.image.load("images/tree.bmp").convert()
# I_BLACK			= pygame.image.load("images/black.bmp").convert()
# I_WATER			= pygame.image.load("images/water.bmp").convert()
# I_ROCK			= pygame.image.load("images/rock.bmp").convert()


def Main():

	font=pygame.font.SysFont(pygame.font.get_default_font(), 25)

	fenetre = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption("RPG")

	text_titre="WELCOME!"
	text_game1="GAME 1"
	text_game2="GAME 2"
	text_game3="GAME 3"
	text_edit="Edit"

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
			game = Game(game_number)
			game.Play(fenetre)
		if edit:
			print("Creating editor")
			edit = Editor()
			print("Editor created")
			edit.Edit(fenetre)

	pygame.quit()



if __name__ == "__main__":
	Main()
