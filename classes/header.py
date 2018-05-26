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

PATH = "/home/leo/ProgrammesPython/rpg/"


a = pygame.init()[1]
while a != 0:
	a = pygame.init()[1]

font = pygame.font.SysFont(pygame.font.get_default_font(), 25)
font2 = pygame.font.SysFont(pygame.font.get_default_font(), 20)

Info = pygame.display.Info()

SCREEN_HEIGHT	= Info.current_h-100
SCREEN_WIDTH	= Info.current_w-100

fenetre = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("RPG")


CELL_WIDTH 			= 20
CELL_HEIGHT  		= 20

ITEM_WIDTH			= 20
ITEM_HEIGHT			= 20

NB_CELLS_SCREEN_X 	= int(SCREEN_WIDTH / CELL_WIDTH + 1)
NB_CELLS_SCREEN_Y	= int(SCREEN_HEIGHT / CELL_HEIGHT + 1)

NB_CELLS_WORLD_X 	= NB_CELLS_SCREEN_X * 10
NB_CELLS_WORLD_Y 	= NB_CELLS_SCREEN_Y * 10

NB_PIX_SCREEN_X   	= NB_CELLS_SCREEN_X * CELL_WIDTH
NB_PIX_SCREEN_Y   	= NB_CELLS_SCREEN_Y * CELL_HEIGHT

WORLD_WIDTH  	= NB_CELLS_WORLD_X * CELL_WIDTH
WORLD_HEIGHT   	= NB_CELLS_WORLD_Y * CELL_HEIGHT

g_fps 			= 30		#g_fps turns per seconds
g_turn_duration	= 1./g_fps	#duration of a turn (in seconds)

cells_list = ["grass", "tree", "water", "rock", "black"]

I_GRASS			= pygame.image.load("images/grass.bmp").convert()
I_TREE			= pygame.image.load("images/tree.bmp").convert()
I_BLACK			= pygame.image.load("images/black.bmp").convert()
I_WATER			= pygame.image.load("images/water.bmp").convert()
I_ROCK			= pygame.image.load("images/rock.bmp").convert()

I_SWORD			= pygame.image.load("images/sword.bmp").convert()
I_ITEM			= pygame.image.load("images/item.bmp").convert()
