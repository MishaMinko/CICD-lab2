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

def test_makeAttack_hit(pygame_init, globals):
    player = Player(globals)
    logicgrid = [[' ' for _ in range(10)] for _ in range(10)]
    posX, posY = globals['pGameGrid'][0][0]
    pygame.mouse.get_pos = lambda: (posX + 25, posY + 25)
    player.makeAttack(globals['pGameGrid'], logicgrid)
    assert logicgrid[0][0] == 'X', "Expected 'X' in logicgrid[0][0] after making a hit"
    assert not player.turn, "Player turn should be set to False after making a hit"
    assert any(token.action == 'Hit' for token in globals['TOKENS']), "A 'Hit' token should be added"