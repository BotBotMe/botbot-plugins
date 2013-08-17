import pytest
from botbotme_plugins.base import DummyApp
from botbotme_plugins.plugins import bangmotivate


@pytest.fixture
def app():
    return DummyApp(test_plugin=bangmotivate.Plugin())


def test_motivate(app):
    app.respond("!m BotBot")
    assert app.responses == ["You're doing good work, BotBot!"]


def test_nomotivate(app):
    app.respond("shouldn't !m === false?")
    assert len(app.responses) == 0
