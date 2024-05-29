import pygame
import pytest
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

def test_makeAttack_miss(pygame_init, globals):
    player = Player(globals)
    logicgrid = [['O' for _ in range(10)] for _ in range(10)]
    posX, posY = globals['pGameGrid'][0][0]
    pygame.mouse.get_pos = lambda: (posX + 25, posY + 25)
    player.makeAttack(globals['pGameGrid'], logicgrid)
    assert logicgrid[0][0] == 'T', "Expected 'T' in logicgrid[0][0] after making a miss"
    assert not player.turn, "Player turn should be set to False after making a miss"
    assert any(token.action == 'Hit' for token in globals['TOKENS']), "A 'Hit' token should be added"

def test_makeAttack_out_grid(pygame_init, globals):
    player = Player(globals)
    logicgrid = [[' ' for _ in range(10)] for _ in range(10)]
    posX, posY = -50, -50
    pygame.mouse.get_pos = lambda: (posX, posY)
    player.makeAttack(globals['pGameGrid'], logicgrid)
    assert all(row == [' ' for _ in range(10)] for row in logicgrid), "No changes should be made to logicgrid"
    assert player.turn, "Player turn should not be changed if attack is outside the grid"

def test_makeAttack_already_hit(pygame_init, globals):
    player = Player(globals)
    logicgrid = [['T' for _ in range(10)] for _ in range(10)]
    posX, posY = globals['pGameGrid'][0][0]
    pygame.mouse.get_pos = lambda: (posX + 25, posY + 25)
    player.makeAttack(globals['pGameGrid'], logicgrid)
    assert all(row == ['T' for _ in range(10)] for row in logicgrid), "No changes should be made to logicgrid"
    assert player.turn, "Player turn should not be changed if attacking an already hit cell"