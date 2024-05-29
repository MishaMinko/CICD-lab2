import pygame
import pytest
from classes.tokens import Token

@pytest.fixture(scope="module")
def pygame_init():
    pygame.init()
    yield
    pygame.quit()

@pytest.fixture
def token_data():
    image = pygame.Surface((10, 10))
    pos = (5, 5)
    action = 'Hit'
    return image, pos, action