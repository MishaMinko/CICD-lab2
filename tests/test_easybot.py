import pytest
import pygame
import random
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

def test_makeAttack(pygame_init, globals, gamelogic):
    easy_computer = EasyComputer(globals)
    easy_computer.turn = True
    original_randint = random.randint
    random.randint = lambda a, b: 0
    globals['TURNTIMER'] = pygame.time.get_ticks() - 4000
    turn_before_attack = easy_computer.turn
    result = easy_computer.makeAttack(gamelogic)
    random.randint = original_randint
    assert turn_before_attack != result, "The turn status should be updated after the attack."
    assert gamelogic[0][0] in ['T', 'X'], "The game logic should be updated at the attack coordinates."
    assert len(globals['TOKENS']) > 0, "The tokens list should be updated after the attack."

@pytest.mark.parametrize("initial_value, expected", [
    (' ', 'X'),
    ('O', 'T'),
])
def test_makeAttack_varied_gamelogic(pygame_init, globals, gamelogic, initial_value, expected):
    easy_computer = EasyComputer(globals)
    gamelogic[0][0] = initial_value
    original_randint = random.randint
    random.randint = lambda a, b: 0
    globals['TURNTIMER'] = pygame.time.get_ticks() - 4000
    easy_computer.makeAttack(gamelogic)
    random.randint = original_randint
    assert gamelogic[0][0] == expected, f"Expected {expected}, but got {gamelogic[0][0]}"
    if expected == 'T':
        assert any(token.action == 'Hit' for token in globals['TOKENS']), "A 'Hit' token should be added."
    else:
        assert any(token.action == 'Miss' for token in globals['TOKENS']), "A 'Miss' token should be added."