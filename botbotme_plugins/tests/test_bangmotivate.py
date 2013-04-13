import pytest
from botbotme_plugins.base import DummyApp
from botbotme_plugins.plugins import bangmotivate


@pytest.fixture
def app():
    dummy_app = DummyApp(test_plugin=bangmotivate.Plugin())
    return dummy_app


def test_motivate(app):
    responses = app.respond("!m BotBot")
    assert responses == ["You're doing good work, BotBot!"]


def test_nomotivate(app):
    responses = app.respond("shouldn't !m === false?")
    assert len(responses) == 0


def test_received_counter(app):
    app.set_config('bangmotivate', {'motivates_received': True})
    responses = app.respond("!m BotBot")
    assert responses == ["You're doing good work, BotBot!"]
    assert(1 == int(app.storage.hget('bangmotivate:BotBot-receives',
                                     'total')))
    assert(1 == int(app.storage.hget('bangmotivate:BotBot-receives',
                                     'from-repl_user')))


def test_given_counter(app):
    app.set_config('bangmotivate', {'motivates_given': True})
    responses = app.respond("!m BotBot")
    assert responses == ["You're doing good work, BotBot!"]
    assert(1 == int(app.storage.get('bangmotivate:repl_user-gtotal')))
