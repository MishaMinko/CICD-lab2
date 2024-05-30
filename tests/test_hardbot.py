import pytest
import pygame
import random
from classes.hardbot import HardComputer


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
    hard_computer = HardComputer(globals)
    result = hard_computer.computerStatus(msg)
    assert isinstance(result, pygame.Surface), f"Expected pygame.Surface, but got {type(result)}"


def test_makeAttack_first_hit(pygame_init, globals, gamelogic):
    hard_computer = HardComputer(globals)
    random.seed(0)
    globals['TURNTIMER'] = pygame.time.get_ticks() - 4000
    gamelogic[6][6] = 'O'
    gamelogic[6][7] = 'O'
    gamelogic[7][6] = 'O'
    hard_computer.makeAttack(gamelogic)
    assert gamelogic[6][6] == 'T'
    assert any(token.action == 'Hit' for token in globals['TOKENS']), "A 'Hit' token should be added."
    assert len(hard_computer.moves) > 0, "Moves should be generated after a hit."
    assert (6, 7) in hard_computer.moves or (7, 6) in hard_computer.moves, "Expected adjacent moves to be generated."


def test_makeAttack_first_miss(pygame_init, globals, gamelogic):
    hard_computer = HardComputer(globals)
    random.seed(0)
    globals['TURNTIMER'] = pygame.time.get_ticks() - 4000
    hard_computer.makeAttack(gamelogic)
    assert gamelogic[6][6] == 'X'
    assert any(token.action == 'Miss' for token in globals['TOKENS']), "A 'Miss' token should be added."
    assert len(hard_computer.moves) == 0, "No moves should be generated after a miss."


def test_makeAttack_hit_after_hit(pygame_init, globals, gamelogic):
    hard_computer = HardComputer(globals)
    hard_computer.moves = [(1, 1)]
    globals['TURNTIMER'] = pygame.time.get_ticks() - 4000
    gamelogic[1][1] = 'O'
    hard_computer.makeAttack(gamelogic)
    assert gamelogic[1][1] == 'T'
    assert any(token.action == 'Hit' for token in globals['TOKENS']), "A 'Hit' token should be added."
    assert (1, 1) not in hard_computer.moves, "The move should be removed after hitting."


def test_makeAttack_after_no_move(pygame_init, globals, gamelogic):
    hard_computer = HardComputer(globals)
    hard_computer.moves = [(1, 1)]
    globals['TURNTIMER'] = pygame.time.get_ticks() - 1000
    gamelogic[1][1] = 'O'
    hard_computer.makeAttack(gamelogic)
    assert gamelogic[1][1] == 'O'
    assert not any(token.action == 'Hit' for token in globals['TOKENS']), "No 'Hit' token should be added if not enough time has passed."
    assert (1, 1) in hard_computer.moves, "The move should not be removed if not enough time has passed."