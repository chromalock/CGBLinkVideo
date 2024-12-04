import serial

import encode.video as video
import encode.tile_encode as tile
import argparse
import time
import sys
import pygame
import threading

from util import chunks

pygame.init()

input_width = 1080
input_height = 720
input_buffer = input_width*input_height

width = 640
height = 480

surface = None
run = True

inbuffer = None


def game_loop():
    global buffer
    global inbuffer
    global surface
    global run

    pygame.display.set_caption("GBLink")
    screen = pygame.display.set_mode([width, height])

    pos_x = 0
    pos_y = 0
    while run:
        screen.fill(pygame.Color(0, 0, 0))
        if surface:
            screen.blit(surface, (pos_x, pos_y))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    pos_x += 15
                elif event.key == pygame.K_LEFT:
                    pos_x -= 15
                elif event.key == pygame.K_UP:
                    pos_y -= 15
                elif event.key == pygame.K_DOWN:
                    pos_y += 15
        pos_x = min(max(pos_x, 0), input_width)
        pos_y = min(max(pos_y, 0), input_height)

    pygame.display.quit()


def read_loop():
    global run
    global inbuffer
    global surface
    while run:
        inbuffer = [(y, y, y) for y in sys.stdin.buffer.read(input_buffer)]
        if inbuffer:
            buffer = bytes([y for pixel in inbuffer for y in pixel])
            surface = pygame.image.frombytes(
                buffer, (input_width, input_height), "RGB")


threading.Thread(target=game_loop).start()
threading.Thread(target=read_loop).start()
