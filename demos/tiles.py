import pygame
import cairo
import sys
import math
import time
import random

scale = 6

width, height = (scale * 160), (scale * 144)

palette = [(0, 0, 0), (83.33, 83.33, 83.33),
           (166.66, 166.66, 166.66), (255, 255, 255)]

pygame.init()
pygame.font.init()
pygame.display.set_mode((width, height))

font = pygame.font.SysFont("Mai10", 15)

surface = pygame.display.get_surface()

pygame.draw.rect(surface, palette[0], (0, 0, width, height))
pygame.display.flip()

t = 8*scale

time.sleep(1)


for k in range(0, 20):
    pygame.draw.rect(surface, palette[0], (0, 0, width, height))
    for y in range(0, 18):
        for x in range(0, 20):
            pygame.draw.rect(surface, palette[3], (x*t, y*t, t, t))
            text_surface = font.render(
                str((random.randint(0, 0xff))), False, palette[0])
            surface.blit(text_surface, (x*t+2, y*t))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
    pygame.display.flip()
    time.sleep(1/2)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
