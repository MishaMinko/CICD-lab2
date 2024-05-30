import pygame
import pytest
from classes.ship import Ship, Guns

@pytest.fixture(scope="module")
def pygame_init():
    pygame.init()
    yield
    pygame.quit()

@pytest.fixture
def globals():
    def load_image_mock(path, size):
        surface = pygame.Surface(size)
        return surface

    return {
        'loadImage': load_image_mock,
        'updateGameScreen': pygame.display.update,
        'GAMESCREEN': pygame.display.set_mode((800, 600)),
    }

@pytest.fixture
def ship_data():
    name = 'Test Ship'
    img = 'ship.png'
    pos = (100, 100)
    size = (50, 100)
    return name, img, pos, size

@pytest.fixture
def gun_data():
    imgPath = 'gun.png'
    pos = (200, 200)
    size = (20, 20)
    offset = 0.5
    return imgPath, pos, size, offset

def test_ship_rotateShip(pygame_init, globals, ship_data):
    name, img, pos, size = ship_data
    ship = Ship(globals, name, img, pos, size)
    assert ship.rotation == False, f"Expected initial rotation to be False, but got {ship.rotation}"
    ship.rotateShip(doRotation=True)
    assert ship.rotation == True, f"Expected rotation to be True after first rotate, but got {ship.rotation}"
    ship.rotateShip(doRotation=True)
    assert ship.rotation == False, f"Expected rotation to be False after second rotate, but got {ship.rotation}"

def test_ship_rotateImageAndRect(pygame_init, globals, ship_data):
    name, img, pos, size = ship_data
    ship = Ship(globals, name, img, pos, size)
    assert ship.image == ship.vImage
    ship.rotateShip(doRotation=True)
    ship.rotateImageAndRect()
    assert ship.image == ship.hImage
    ship.rotateShip(doRotation=True)
    ship.rotateImageAndRect()
    assert ship.image == ship.vImage

def test_ship_checkForCollisions(pygame_init, globals, ship_data):
    name, img, pos, size = ship_data
    ship = Ship(globals, name, img, pos, size)
    ship2 = Ship(globals, name, img, pos, size)
    ship3 = Ship(globals, name, img, (50, 100), size)
    assert ship.checkForCollisions([ship, ship2]) == True
    assert ship.checkForCollisions([ship, ship3]) == False

def test_ship_magnetToGridEdge(pygame_init, globals, ship_data):
    name, img, pos, size = ship_data
    ship = Ship(globals, name, img, pos, size)
    gridCoords = [[(i*50, j*50) for i in range(10)] for j in range(10)]
    CELLSIZE = 50
    ship.rect.right = 475
    ship.rect.bottom = 530
    ship.magnetToGridEdge(gridCoords, CELLSIZE)
    assert ship.rect.centerx == 450
    assert ship.rect.bottom == 500