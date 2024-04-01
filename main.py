#Програма написана Фурсенком Михайлом та Полярушом Данилом групи ІПЗ-22
import pygame
import random
pygame.init()


#game functions
def createGameGrid(rows, cols, cellsize, pos):
    startX = pos[0]
    startY = pos[1]
    coordGrid = []
    for _ in range(rows):
        rowX = []
        for _ in range(cols):
            rowX.append((startX, startY))
            startX += cellsize
        coordGrid.append(rowX)
        startX = pos[0]
        startY += cellsize
    return coordGrid


def createGameLogic(rows, cols):
    gameLogic = []
    for _ in range(rows):
        rowX = []
        for _ in range(cols):
            rowX.append(' ')
        gameLogic.append(rowX)
    return gameLogic


def showGridOnScreen(window, cellsize, pGrid, cGrid):
    gameGrids = [pGrid, cGrid]
    for grid in gameGrids:
        for row in grid:
            for col in row:
                pygame.draw.rect(window, (255, 255, 255), (col[0], col[1], cellsize, cellsize), 1)


def printGameLogic():
    print('Player Grid'.center(50, '#'))
    for _ in pGameLogic:
        print(_)
    print('Computer Grid'.center(50, '#'))
    for _ in cGameLogic:
        print(_)


def updateGameScreen(window):
    window.fill((0, 0, 0))

    showGridOnScreen(window, CELLSIZE, pGameGrid, cGameGrid)

    pygame.display.update()


#game settings
SCREENWIDTH = 1260
SCREENHEIGHT = 960
ROWS = 10
COLS = 10
CELLSIZE = 50


#pygame display
GAMESCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.set_caption('BattleShip')


#creating game variables
pGameGrid = createGameGrid(ROWS, COLS, CELLSIZE, (50, 50))
pGameLogic = createGameLogic(ROWS, COLS)

cGameGrid = createGameGrid(ROWS, COLS, CELLSIZE, (SCREENWIDTH - (ROWS * CELLSIZE) - 50, 50))
cGameLogic = createGameLogic(ROWS, COLS)

printGameLogic()


#game flow
RUNGAME = True
while RUNGAME:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNGAME = False
    
    updateGameScreen(GAMESCREEN)

pygame.quit()