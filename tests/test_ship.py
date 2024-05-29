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
    return {
        'loadImage': pygame.image.load,
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