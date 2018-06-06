#!/usr/bin/python3.5
# -*-coding:utf-8 -*

from __future__ import division

import os as os
import sys as sys
import pygame as pygame
from pygame.locals import *

import math as m
import time as time
import random as rand

import pickle
from pathlib import Path

PATH = "/home/leo/ProgrammesPython/rpg/"


a = pygame.init()[1]
while a != 0:
	a = pygame.init()[1]

font = pygame.font.SysFont(pygame.font.get_default_font(), 25)
font2 = pygame.font.SysFont(pygame.font.get_default_font(), 20)
font50 = pygame.font.SysFont(pygame.font.get_default_font(), 50)

# fenetre = pygame.display.set_mode((0, 0), pygame.RESIZABLE | pygame.FULLSCREEN)
fenetre = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# fenetre = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("RPG")

Info = pygame.display.Info()

SCREEN_HEIGHT	= Info.current_h - 100
SCREEN_WIDTH	= Info.current_w - 100



CELL_WIDTH 			= 20
CELL_HEIGHT  		= 20

ITEM_WIDTH			= 20
ITEM_HEIGHT			= 20

NB_CELLS_SCREEN_X 	= int(SCREEN_WIDTH / CELL_WIDTH + 1)
NB_CELLS_SCREEN_Y	= int(SCREEN_HEIGHT / CELL_HEIGHT + 1)

NB_CELLS_WORLD_X 	= 500
NB_CELLS_WORLD_Y 	= 500
print(NB_CELLS_WORLD_X, NB_CELLS_WORLD_Y)

NB_PIX_SCREEN_X   	= NB_CELLS_SCREEN_X * CELL_WIDTH
NB_PIX_SCREEN_Y   	= NB_CELLS_SCREEN_Y * CELL_HEIGHT

WORLD_WIDTH  	= NB_CELLS_WORLD_X * CELL_WIDTH
WORLD_HEIGHT   	= NB_CELLS_WORLD_Y * CELL_HEIGHT

g_fps 			= 30		#g_fps turns per seconds
g_turn_duration	= 1./g_fps	#duration of a turn (in seconds)


world_images_folder = "data/images/world/"
items_images_folder = "data/images/items/"
perso_images_folder = "data/images/characters/perso/"
characters_images_folder = "data/images/characters/"

images_dict = {	"I_GRASS"			: pygame.image.load(world_images_folder + "grass.bmp").convert(),
				"I_TREE"			: pygame.image.load(world_images_folder + "tree.bmp").convert(),
				"I_BLACK"			: pygame.image.load(world_images_folder + "black.bmp").convert(),
				"I_WATER"			: pygame.image.load(world_images_folder + "water.bmp").convert(),
				"I_ROCK"			: pygame.image.load(world_images_folder + "rock.bmp").convert(),
				"I_WOOD"			: pygame.image.load(world_images_folder + "wood.bmp").convert(),
				"I_PLANCK"			: pygame.image.load(world_images_folder + "planck.bmp").convert(),
				"I_SAND"			: pygame.image.load(world_images_folder + "sand.bmp").convert(),


				"I_SWORD"			: pygame.image.load(items_images_folder + "sword.bmp").convert(),
				"I_ITEM"			: pygame.image.load(items_images_folder + "item.bmp").convert(),


				"I_PERSO_S_1"		: pygame.image.load(perso_images_folder + "perso_S_1.bmp").convert_alpha(),
				"I_PERSO_S_2"		: pygame.image.load(perso_images_folder + "perso_S_2.bmp").convert_alpha(),
				"I_PERSO_E_1"		: pygame.image.load(perso_images_folder + "perso_E_1.bmp").convert_alpha(),
				"I_PERSO_E_2"		: pygame.image.load(perso_images_folder + "perso_E_2.bmp").convert_alpha(),
				"I_PERSO_W_1"		: pygame.image.load(perso_images_folder + "perso_W_1.bmp").convert_alpha(),
				"I_PERSO_W_2"		: pygame.image.load(perso_images_folder + "perso_W_2.bmp").convert_alpha(),
				"I_PERSO_N_1"		: pygame.image.load(perso_images_folder + "perso_N_1.bmp").convert_alpha(),
				"I_PERSO_N_2"		: pygame.image.load(perso_images_folder + "perso_N_2.bmp").convert_alpha(),

				"I_PNG"				: pygame.image.load(characters_images_folder + "default_character.bmp").convert_alpha()
				}

images_dict["I_SWORD"].set_colorkey((0,0,255))
images_dict["I_ITEM"].set_colorkey((0,0,255))
