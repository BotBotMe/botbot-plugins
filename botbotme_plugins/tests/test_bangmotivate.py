import pytest
from botbotme_plugins.base import DummyApp
from botbotme_plugins.plugins import bangmotivate


@pytest.fixture
def app():
    return DummyApp(test_plugin=bangmotivate.Motivate())


def test_motivate(app):
    responses = app.respond("!m BotBot")
    assert responses == ["You're doing good work, BotBot!"]


def test_nomotivate(app):
    responses = app.respond("shouldn't !m === false?")
    assert len(responses) == 0
