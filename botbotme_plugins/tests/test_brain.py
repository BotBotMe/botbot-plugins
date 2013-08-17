# -*- coding: utf-8 -*-
import pytest
from botbotme_plugins.base import DummyApp
from botbotme_plugins.plugins import brain


@pytest.fixture
def app():
    return DummyApp(test_plugin=brain.Plugin())


def test_remember(app):
    app.respond(u"@shrug=¯\_(ツ)_/¯")
    assert app.responses == [u'I will remember "shrug" for you repl_user.']
    app.respond(ur"@shrug ?")
    assert app.responses == [u"¯\_(ツ)_/¯"]
