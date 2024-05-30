import pygame, random, os, pytest
from main import createGameGrid, createGameLogic, updateGameLogic, randomizeShipPositions, checkForWinners, loadImage, Ship

@pytest.fixture(scope="module")
def pygame_init():
    pygame.init()
    yield
    pygame.quit()

@pytest.fixture
def game_grid():
    rows, cols, cellsize, pos = 10, 10, 50, (0, 0)
    return createGameGrid(rows, cols, cellsize, pos)

@pytest.fixture
def game_logic():
    rows, cols = 10, 10
    return createGameLogic(rows, cols)

@pytest.fixture
def fleet():
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
    fleet = []
    for name in FLEET.keys():
        fleet.append(Ship(globals(),name, FLEET[name][1], FLEET[name][2], FLEET[name][3], FLEET[name][4], FLEET[name][5], FLEET[name][6], FLEET[name][7]))
    return fleet