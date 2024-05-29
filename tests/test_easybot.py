import pytest
import pygame
from classes.easybot import EasyComputer

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
        'BLUETOKEN': pygame.Surface((10, 10)),
        'pGameGrid': [[(x, y) for x in range(10)] for y in range(10)],
        'cGameGrid': [[(x, y) for x in range(10)] for y in range(10)],
        'CELLSIZE': 50
    }

@pytest.fixture
def gamelogic():
    return [[' ' for _ in range(10)] for _ in range(10)]

@pytest.mark.parametrize("msg", [
    "Thinking",
    "Attacking",
    "",
])
def test_computerStatus(pygame_init, globals, msg):
    easy_computer = EasyComputer(globals)
    result = easy_computer.computerStatus(msg)
    assert isinstance(result, pygame.Surface), f"Expected pygame.Surface, but got {type(result)}"

