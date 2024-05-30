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


def test_token_draw(pygame_init, token_data):
    image, pos, action = token_data
    token = Token(image, pos, action)
    mock_window = pygame.Surface((100, 100))
    token.draw(mock_window)
    assert mock_window.get_at(pos) == (0, 0, 0, 255), "Expected token to be drawn at the correct position"