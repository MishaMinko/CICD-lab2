#Програма написана Фурсенком Михайлом та Полярушом Данилом групи ІПЗ-22
from classes.ship import Ship
import pygame, random, os
pygame.init()


class GameUpdater:
    def __init__(self):
        self.window = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

    def updateGameScreen(self):
        self.window.fill((0, 0, 0))

        showGridOnScreen(self.window, CELLSIZE, pGameGrid, cGameGrid)

        for ship in pFleet:
            ship.draw(self.window)
            ship.magnetToGridEdge(pGameGrid, CELLSIZE)
            ship.magnetToGrid(pGameGrid, CELLSIZE)

        for ship in cFleet:
            ship.draw(self.window)
            ship.magnetToGridEdge(cGameGrid, CELLSIZE)
            ship.magnetToGrid(cGameGrid, CELLSIZE)

        pygame.display.update()


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


def loadImage(path, size, rotate=False):
    img = pygame.image.load(path).convert_alpha()
    img = pygame.transform.scale(img, size)
    if rotate == True:
        img = pygame.transform.rotate(img, -90)
    return img


def sortFleet(ship, shiplist):
    shiplist.remove(ship)
    shiplist.append(ship)


def randomizeShipPositions(shiplist, gamegrid):
    placedShips = []
    for _, ship in enumerate(shiplist):
        validPosition = False
        while validPosition == False:
            ship.setDefaultPosition()
            rotateShip = random.choice([True, False])
            if rotateShip == True:
                yAxis = random.randint(0, 9)
                xAxis = random.randint(0, 9 - (ship.hImage.get_width()//50))
                ship.rotateShip(True)
            else:
                yAxis = random.randint(0, 9 - (ship.vImage.get_height()//50))
                xAxis = random.randint(0, 9)
            ship.rect.topleft = gamegrid[yAxis][xAxis]
            if len(placedShips) > 0:
                for item in placedShips:
                    if ship.rect.colliderect(item.rect):
                        validPosition = False
                        break
                    else:
                        validPosition = True
            else:
                validPosition = True
        placedShips.append(ship)


def createFleet():
    fleet = []
    for name in FLEET.keys():
        fleet.append(Ship(name, FLEET[name][1], FLEET[name][2], FLEET[name][3], FLEET[name][4], FLEET[name][5], FLEET[name][6], FLEET[name][7]))
    return fleet


#game settings
SCREENWIDTH = 1260
SCREENHEIGHT = 960
ROWS = 10
COLS = 10
CELLSIZE = 50


#pygame display
updater = GameUpdater()
pygame.display.set_caption('BattleShip')

current_directory = os.path.dirname(__file__)
FLEET = {
    'battleship': ['battleship', os.path.join(current_directory, 'assets', 'images', 'ships', 'battleship', 'battleship.png'), (125, 600), (40, 195),
                   4, os.path.join(current_directory, 'assets', 'images', 'ships', 'battleship', 'battleshipgun.png'), (0.4, 0.125), [-0.525, -0.34, 0.67, 0.49]],
    'cruiser': ['cruiser', os.path.join(current_directory, 'assets', 'images', 'ships', 'cruiser', 'cruiser.png'), (200, 600), (40, 195),
                2, os.path.join(current_directory, 'assets', 'images', 'ships', 'cruiser', 'cruisergun.png'), (0.4, 0.125), [-0.36, 0.64]],
    'destroyer': ['destroyer', os.path.join(current_directory, 'assets', 'images', 'ships', 'destroyer', 'destroyer.png'), (275, 600), (30, 145),
                  2, os.path.join(current_directory, 'assets', 'images', 'ships', 'destroyer', 'destroyergun.png'), (0.5, 0.15), [-0.52, 0.71]],
    'patrol boat': ['patrol boat', os.path.join(current_directory, 'assets', 'images', 'ships', 'patrol boat', 'patrol boat.png'), (425, 600), (20, 95),
                    0, '', None, None],
    'submarine': ['submarine', os.path.join(current_directory, 'assets', 'images', 'ships', 'submarine', 'submarine.png'), (350, 600), (30, 145),
                  1, os.path.join(current_directory, 'assets', 'images', 'ships', 'submarine', 'submarinegun.png'), (0.25, 0.125), [-0.45]],
    'carrier': ['carrier', os.path.join(current_directory, 'assets', 'images', 'ships', 'carrier', 'carrier.png'), (50, 600), (45, 245),
                0, '', None, None],
    'rescue ship': ['rescue ship', os.path.join(current_directory, 'assets', 'images', 'ships', 'rescue ship', 'rescue ship.png'), (500, 600), (20, 95),
                    0, '', None, None]
}


#creating game variables
pGameGrid = createGameGrid(ROWS, COLS, CELLSIZE, (50, 50))
pGameLogic = createGameLogic(ROWS, COLS)
pFleet = createFleet()

cGameGrid = createGameGrid(ROWS, COLS, CELLSIZE, (SCREENWIDTH - (ROWS * CELLSIZE) - 50, 50))
cGameLogic = createGameLogic(ROWS, COLS)
cFleet = createFleet()
randomizeShipPositions(cFleet, cGameGrid)

printGameLogic()


#game flow
RUNGAME = True
while RUNGAME:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNGAME = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for ship in pFleet:
                    if ship.rect.collidepoint(pygame.mouse.get_pos()):
                        ship.active = True
                        sortFleet(ship, pFleet)
                        ship.selectShipAndMove(updater, pFleet)
    
    updater.updateGameScreen()

pygame.quit()