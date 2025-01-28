import pygame as pg
import sys
import time

W = 400
H = 300

sc = pg.display.set_mode((W, H))
sc.fill((100, 150, 200))

dog_surf = pg.image.load('heart.png')
