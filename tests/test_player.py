import pygame
import pytest
from classes.tokens import Token
from classes.player import Player

@pytest.fixture(scope="module")
def pygame_init():
    pygame.init()
    yield
    pygame.quit()

@pytest.fixture
def globals():
    return {
        'TURNTIMER': 0,
        'TOKENS': [],
        'REDTOKEN': pygame.Surface((10, 10)),
        'GREENTOKEN': pygame.Surface((10, 10)),
        'pGameGrid': [[(x, y) for x in range(10)] for y in range(10)],
        'cGameGrid': [[(x, y) for x in range(10)] for y in range(10)],
        'CELLSIZE': 50
    }