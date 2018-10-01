import time
import sys
import pygame
from pygame import gfxdraw


# this function was found in some old code i made
# display: name of the pygame screen
# st_pos: starting position in the form [x pixel coordinate, y pixel coordinate]
# b_len: pixel length of border, must be at least 1
# num: how many lines to draw in the form [vertical lines, horizontal lines], must be at least 2
# col: colour of the lines
def draw_grid(display, st_pos, b_len, num, col):
    # input check
    if b_len[0] < 1 or b_len[1] < 1 or num[0] < 2 or num[1] < 2:
        raise ValueError('draw_grid() called with invalid arguments for length or number of lines')

    # lock screen, this might make it faster to draw stuff? idk
    display.lock()
    # separation for vertical, horizontal lines
    sep = [b_len[0] // num[0] + 1, b_len[1] // num[1] + 1]

    # vertical lines
    for i in range(num[0] + 1):
        pygame.draw.line(display, col, (st_pos[0] + sep[0] * i, st_pos[1]),
                         (st_pos[0] + sep[0] * i, st_pos[1] + sep[1] * num[1]))
    # horizontal lines
    for i in range(num[1] + 1):
        pygame.draw.line(display, col, (st_pos[0], st_pos[1] + sep[1] * i),
                         (st_pos[0] + sep[0] * num[0], st_pos[1] + sep[1] * i))

# ---- SETUP ----

# setup pygame
pygame.init()
pygame.font.init()
time.sleep(0.5)

# setup display and clock
clock = pygame.time.Clock()
disL = 1000
disH = 600
screen = pygame.display.set_mode((disL, disH))
pygame.display.set_caption("Route-simulation")

# variables
# i/o variables
mousePos = []

# general map variables
mapPos = [50, 50]
mapLen = [3, 3]  # width, height
mapL = 3
mapH = 3


# ---- LOOP ----
while True:
    # should make it 60FPS max
    clock.tick(60)

    # background
    screen.fill((250, 250, 250))

    # get input
    mousePressed = [0, 0, 0]  # reset mouse presses
    mousePos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePressed = pygame.mouse.get_pressed()

    draw_grid(screen, [50, 50], [400, 200], [8, 4], (0, 0, 0))

    # update display!
    pygame.display.update()

