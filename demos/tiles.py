import pygame
import cairo
import sys
import math
import time

width, height = 160, 144

palette = [(0, 0, 0), (83.33, 83.33, 83.33),
           (166.66, 166.66, 166.66), (255, 255, 255)]

pygame.init()
pygame.font.init()
pygame.display.set_mode((width, height))

font = pygame.font.SysFont("Mai10", 5)

surface = pygame.display.get_surface()

pygame.draw.rect(surface, palette[0], (0, 0, width, height))
pygame.display.flip()

t = 8

for y in range(0, 18):
    for x in range(0, 20):
        pygame.draw.rect(surface, palette[3], (x*t, y*t, t, t))
        # text_surface = font.render(
        #     hex((y * 20 + x) % 0xff)[2:], False, palette[0])
        # surface.blit(text_surface, (x*t, y*t-3))
        time.sleep(1/20)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
