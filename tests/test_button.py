import pytest
import pygame
from classes.button import Button


@pytest.fixture(scope="module")
def pygame_init():
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def dummy_surface():
    return pygame.Surface((100, 50))


@pytest.fixture
def dummy_window():
    return pygame.Surface((200, 100))


@pytest.fixture
def button(dummy_surface):
    size = (100, 50)
    pos = (0, 0)
    msg = "Test"
    return Button(dummy_surface, size, pos, msg)


@pytest.mark.parametrize("msg", [
    "Hello World",
    "Привіт",
    "123",
    "!@#",
    ""
])
def test_addText(pygame_init, button, msg):
    try:
        result = button.addText(msg)
        if not isinstance(result, pygame.Surface):
            pytest.fail(f"Expected pygame.Surface, but got {type(result)}")
    except Exception as e:
        pytest.fail(f"Function raised an exception: {e}")


def test_focusOnButton(pygame_init, button, dummy_window):
    try:
        pygame.mouse.set_pos((50, 25))
        button.focusOnButton(dummy_window)
        pygame.mouse.set_pos((150, 75))
        button.focusOnButton(dummy_window)
    except Exception as e:
        pytest.fail(f"Function raised an exception: {e}")


@pytest.mark.parametrize("initial_name, gameStatus, expected_name", [
    ("Deploy", False, "Quit"),
    ("Quit", True, "Deploy"),
    ("Randomize", False, "Redeploy"),
    ("Redeploy", True, "Randomize"),
])
def test_updateButtons(pygame_init, dummy_surface, initial_name, gameStatus, expected_name):
    button = Button(dummy_surface, (100, 50), (0, 0), initial_name)
    try:
        button.updateButtons(gameStatus)
        if button.name != expected_name:
            pytest.fail(f"Expected name '{expected_name}', but got '{button.name}'")
    except Exception as e:
        pytest.fail(f"Function raised an exception: {e}")


def test_draw(pygame_init, button, dummy_window):
    try:
        button.draw(dummy_window, True)
        button.draw(dummy_window, False)
    except Exception as e:
        pytest.fail(f"Function raised an exception: {e}")
