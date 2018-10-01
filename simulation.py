import time
import sys
import pygame
from pygame import gfxdraw


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
    display.unlock()


# creates some text centered on an x y coordinate
def create_text(display, location, text, centered, font, col):
    display_text = font.render(str(text), True, col)
    text_rect = display_text.get_rect()
    if centered:
        display.blit(display_text, (location[0] - text_rect[2] // 2, location[1] - text_rect[3] // 2))
    else:
        display.blit(display_text, (location[0], location[1] - text_rect[3] // 2))


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

# images
imgPlus = pygame.image.load("plus-sign.png").convert_alpha()
imgMinus = pygame.image.load("minus-sign.png").convert_alpha()

# fonts
defFont = pygame.font.SysFont('Trebuchet MS', 24, False)

# colours
colInc = [220, 220, 220]
colDec = [220, 220, 220]
colGrid = [0, 0, 0]

# variables
# i/o variables
mousePos = []

# general map variables
mapPos = [75, 50]
mapLen = [550, 500]  # width, height
numLines = [3, 3]  # vertical, horizontal lines

# button rect objects
# increase/decrease number of vertical lines (min 2)
butDecVert = pygame.Rect(775, disH // 2 - 125, 50, 50)
butIncVert = pygame.Rect(850, disH // 2 - 125, 50, 50)
# increase/decrease number of horizontal lines (min 2)
butDecHor = pygame.Rect(775, disH // 2 + 100, 50, 50)
butIncHor = pygame.Rect(850, disH // 2 + 100, 50, 50)

listOfBut = [butDecVert, butIncVert, butDecHor, butIncHor]  # list for easier access

# ---- LOOP ----
while True:
    # should make it 60FPS max
    clock.tick(60)

    # get input
    mousePressed = [0, 0, 0]  # reset mouse presses
    mousePos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePressed = pygame.mouse.get_pressed()

    # background
    screen.fill((250, 250, 250))

    # main grid
    draw_grid(screen, mapPos, mapLen, numLines, colGrid)

    # draw buttons
    for i in range(len(listOfBut)):
        if i % 2 == 0:  # red decrease
            pygame.draw.rect(screen, colDec, listOfBut[i])
            screen.blit(imgMinus, (listOfBut[i][0], listOfBut[i][1]))
        else:  # green increase
            pygame.draw.rect(screen, colInc, listOfBut[i])
            screen.blit(imgPlus, (listOfBut[i][0], listOfBut[i][1]))
        pygame.draw.rect(screen, (0, 0, 0), listOfBut[i], 1)

    # display num rows and columns
    create_text(screen, (butIncVert[0] - 15, butIncVert[1] - 25),
                "Length: " + str(numLines[0]), True, defFont, (0, 0, 0))
    create_text(screen, (butIncHor[0] - 15, butIncHor[1] - 25),
                "Height: " + str(numLines[1]), True, defFont, (0, 0, 0))

    # increase and decrease number of rows and columns
    for i in range(len(listOfBut)):
        if listOfBut[i].collidepoint(mousePos[0], mousePos[1]):
            pygame.draw.rect(screen, (0, 0, 0), listOfBut[i], 3)
            if mousePressed[0] == 1:  # USER PRESSED BUTTON AAAH
                # dec ver, inc ver, dec hor, inc hor
                if i == 0 and numLines[0] > 2:
                    numLines[0] -= 1
                elif i == 1:
                    numLines[0] += 1
                elif i == 2 and numLines[1] > 2:
                    numLines[1] -= 1
                elif i  == 3 and numLines[1] > 2:
                    numLines[1] += 1

    # update display!
    pygame.display.update()
