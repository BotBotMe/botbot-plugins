# -*- coding: utf-8 -*-
import pytest
from botbot_plugins.base import DummyApp
from botbot_plugins.plugins import brain


@pytest.fixture
def app():
    return DummyApp(test_plugin=brain.Plugin())


def test_remember(app):
    responses = app.respond(u"@shrug=¯\_(ツ)_/¯")
    assert responses == [u'I will remember "shrug" for you repl_user.']
    responses = app.respond(ur"@shrug ?")
    assert responses == [u"¯\_(ツ)_/¯"]
