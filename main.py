# Програма написана Фурсенком Михайлом та Полярушом Данилом групи ІПЗ-22 та Іллею Кравчуком ІПЗ-24
from classes.ship import Ship
from classes.button import Button
from classes.player import Player
from classes.easybot import EasyComputer
from classes.hardbot import HardComputer
import pygame, random, os
pygame.init()


# game functions
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


def updateGameLogic(coordGrid, shiplist, gamelogic, cellsize):
    for i, rowX in enumerate(coordGrid):
        for j, colX in enumerate(rowX):
            if gamelogic[i][j] != 'T' and gamelogic[i][j] != 'X':
                gamelogic[i][j] = ' '
                for ship in shiplist:
                    if pygame.rect.Rect(colX[0], colX[1], cellsize, cellsize).colliderect(ship.rect):
                        gamelogic[i][j] = 'O'


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


def resetShips(shiplist):
    if DEPLOYMENT == True:
        for ship in shiplist:
            ship.setDefaultPosition()


def randomizeShipPositions(shiplist, gamegrid):
    placedShips = []
    for _, ship in enumerate(shiplist):
        validPosition = False
        while validPosition == False:
            ship.setDefaultPosition()
            rotateShip = random.choice([True, False])
            if rotateShip == True:
                yAxis = random.randint(0, 9)
                xAxis = random.randint(0, 9 - (ship.hImage.get_width() // 50))
                ship.rotateShip(True)
            else:
                yAxis = random.randint(0, 9 - (ship.vImage.get_height() // 50))
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
        fleet.append(Ship(globals(), name, FLEET[name][1], FLEET[name][2], FLEET[name][3], FLEET[name][4], FLEET[name][5], FLEET[name][6], FLEET[name][7]))
    return fleet


def deploymentPhase(depl):
    if depl == True:
        return False
    else:
        return True


def restartGame(DEPLOYMENT):
    TOKENS.clear()
    resetShips(pFleet)
    randomizeShipPositions(cFleet, cGameGrid)
    updateGameLogic(cGameGrid, cFleet, cGameLogic, CELLSIZE)
    updateGameLogic(pGameGrid, pFleet, pGameLogic, CELLSIZE)

    DEPLOYMENT = deploymentPhase(DEPLOYMENT)


def takeTurns(p1, p2):
    if p1.turn == True:
        p2.turn = False
    else:
        p2.turn = True
        if not p2.makeAttack(pGameLogic):
            p1.turn = True


def checkForWinners(grid):
    for row in grid:
        if 'O' in row:
            return False
    return True


def mainMenuScreen(window):
    window.blit(MAINMENUIMAGE, (0, 0))

    for button in difficulty_buttons:
        button.draw(window, None)

    font = pygame.font.SysFont('Stencil', 48)
    title_text = font.render("Choose Difficulty", True, (255, 255, 255))
    window.blit(title_text, (SCREENWIDTH // 2 - title_text.get_width() // 2, 100))


def deploymentScreen(window):
    showGridOnScreen(window, CELLSIZE, pGameGrid, cGameGrid)

    for ship in pFleet:
        ship.draw(window)
        ship.magnetToGridEdge(pGameGrid, CELLSIZE)
        ship.magnetToGrid(pGameGrid, CELLSIZE)

    for ship in cFleet:
        ship.magnetToGridEdge(cGameGrid, CELLSIZE)
        ship.magnetToGrid(cGameGrid, CELLSIZE)

    for button in BUTTONS:
        button.draw(window, DEPLOYMENT)

    for token in TOKENS:
        token.draw(window)

    updateGameLogic(pGameGrid, pFleet, pGameLogic, CELLSIZE)
    updateGameLogic(cGameGrid, cFleet, cGameLogic, CELLSIZE)


def endScreen(window):
    restartGame(DEPLOYMENT)

    window.blit(ENDSCREENIMAGE, (0, 0))

    for button in difficulty_buttons:
        button.draw(window, None)

    font = pygame.font.SysFont('Stencil', 48)
    title_text = font.render(winner, True, (255, 255, 255))
    window.blit(title_text, (SCREENWIDTH // 2 - title_text.get_width() // 2, 100))


def updateGameScreen(window):
    window.fill((0, 0, 0))

    if GAMESTATE == STAGE[0]:
        mainMenuScreen(window)
    elif GAMESTATE == STAGE[1]:
        deploymentScreen(window)
    elif GAMESTATE == STAGE[2]:
        endScreen(window)

    pygame.display.update()


def main():
    global SCREENWIDTH, SCREENHEIGHT, ROWS, COLS, CELLSIZE, DEPLOYMENT, TURNTIMER, GAMESTATE, GAMESCREEN
    global FLEET, STAGE, MAINMENUIMAGE, ENDSCREENIMAGE, BUTTONS, difficulty_buttons, REDTOKEN, GREENTOKEN, BLUETOKEN, TOKENS
    global pGameGrid, pGameLogic, pFleet, cGameGrid, cGameLogic, cFleet, player1, computer, winner

    # game settings
    SCREENWIDTH = 1260
    SCREENHEIGHT = 960
    ROWS = 10
    COLS = 10
    CELLSIZE = 50
    DEPLOYMENT = True
    TURNTIMER = pygame.time.get_ticks()
    GAMESTATE = 'Main Menu'

    # pygame displaying
    GAMESCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
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
    STAGE = ['Main Menu', 'Deployment', 'Game Over']

    MAINMENUIMAGE = loadImage(os.path.join(current_directory, 'assets', 'images', 'background', 'Battleship.jpg'), (SCREENWIDTH // 3 * 2, SCREENHEIGHT))
    ENDSCREENIMAGE = loadImage(os.path.join(current_directory, 'assets', 'images', 'background', 'Carrier.jpg'), (SCREENWIDTH, SCREENHEIGHT))
    BUTTONIMAGE = loadImage(os.path.join(current_directory, 'assets', 'images', 'buttons', 'button.png'), (150, 50))
    BUTTONIMAGE1 = loadImage(os.path.join(current_directory, 'assets', 'images', 'buttons', 'button.png'), (250, 100))
    BUTTONS = [
        Button(BUTTONIMAGE, (150, 50), (25, 900), 'Randomize'),
        Button(BUTTONIMAGE, (150, 50), (200, 900), 'Reset'),
        Button(BUTTONIMAGE, (150, 50), (375, 900), 'Deploy')
    ]
    difficulty_buttons = [
        Button(BUTTONIMAGE1, (250, 100), (900, SCREENHEIGHT // 2 - 150), 'Easy Bot'),
        Button(BUTTONIMAGE1, (250, 100), (900, SCREENHEIGHT // 2 + 150), 'Hard Bot')
    ]
    REDTOKEN = loadImage(os.path.join(current_directory, 'assets', 'images', 'tokens', 'redtoken.png'), (CELLSIZE, CELLSIZE))
    GREENTOKEN = loadImage(os.path.join(current_directory, 'assets', 'images', 'tokens', 'greentoken.png'), (CELLSIZE, CELLSIZE))
    BLUETOKEN = loadImage(os.path.join(current_directory, 'assets', 'images', 'tokens', 'bluetoken.png'), (CELLSIZE, CELLSIZE))
    TOKENS = []

    # creating game variables
    pGameGrid = createGameGrid(ROWS, COLS, CELLSIZE, (50, 50))
    pGameLogic = createGameLogic(ROWS, COLS)
    pFleet = createFleet()

    cGameGrid = createGameGrid(ROWS, COLS, CELLSIZE, (SCREENWIDTH - (ROWS * CELLSIZE) - 50, 50))
    cGameLogic = createGameLogic(ROWS, COLS)
    cFleet = createFleet()
    randomizeShipPositions(cFleet, cGameGrid)

    printGameLogic()

    player1 = Player(globals())
    computer = EasyComputer(globals())

    winner = None

    # game flow
    RUNGAME = True
    while RUNGAME:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNGAME = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if DEPLOYMENT == True:
                        for ship in pFleet:
                            if ship.rect.collidepoint(pygame.mouse.get_pos()):
                                ship.active = True
                                sortFleet(ship, pFleet)
                                ship.selectShipAndMove(pFleet)

                    else:
                        if player1.turn == True:
                            player1.makeAttack(cGameGrid, cGameLogic)
                            if player1.turn == False:
                                TURNTIMER = pygame.time.get_ticks()

                    if GAMESTATE == STAGE[0] or GAMESTATE == STAGE[2]:
                        for button in difficulty_buttons:
                            if button.rect.collidepoint(pygame.mouse.get_pos()):
                                if button.name == 'Easy Bot':
                                    computer = EasyComputer(globals())
                                elif button.name == 'Hard Bot':
                                    computer = HardComputer(globals())
                                GAMESTATE = STAGE[1]
                    elif GAMESTATE == STAGE[1]:
                        for button in BUTTONS:
                            if button.rect.collidepoint(pygame.mouse.get_pos()):
                                if button.name == 'Deploy':
                                    DEPLOYMENT = deploymentPhase(DEPLOYMENT)
                                elif button.name == 'Redeploy':
                                    restartGame(DEPLOYMENT)
                                elif button.name == 'Quit':
                                    RUNGAME = False
                                elif button.name == 'Randomize':
                                    randomizeShipPositions(pFleet, pGameGrid)
                                    randomizeShipPositions(cFleet, cGameGrid)
                                elif button.name == 'Reset':
                                    resetShips(pFleet)
                elif event.button == 2:
                    printGameLogic()
        updateGameScreen(GAMESCREEN)
        if GAMESTATE == STAGE[1] and DEPLOYMENT != True:
            player1Wins = checkForWinners(cGameLogic)
            computerWins = checkForWinners(pGameLogic)
            if player1Wins == True or computerWins == True:
                GAMESTATE = STAGE[2]
                if player1Wins == True:
                    winner = 'Player won!'
                elif computerWins == True:
                    winner = 'Computer won!'

        takeTurns(player1, computer)

    pygame.quit()


if __name__ == "__main__":
    main()
