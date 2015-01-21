# -*- coding: utf-8 -*-
"""
Message service tests
"""
import pytest
from botbot_plugins.base import DummyApp
from botbot_plugins.plugins import message_service


@pytest.fixture
def app():
    return DummyApp(test_plugin=message_service.Plugin())


def test_remember(app):
    """
    [d__d]: message user foobar
    """
    responses = app.respond(r'@message george Are you going to the meeting?')
    assert responses == [u'repl_user, I will tell george when they appear online.']


def test_remind_user(app):
    """
    The user should be messaged when joining the channel
    """
    responses = app.respond(r'@message george Are you going to the meeting?')
    assert responses == [u'repl_user, I will tell george when they appear online.']

    responses = app.respond('george joined the channel', **{
        'Command': 'JOIN',
        'User': 'george'})
    assert responses == ["Beep BEEP! You received the following messages in #dummy-channel when you were offline.\nFrom repl_user 'Are you going to the meeting?'"]

def test_multiple_reminders(app):
    """
    Multiple reminders should work too.
    """
    responses = app.respond(r'@message george Are you going to the meeting?')
    responses = app.respond(r'@message george I think I will be going.')

    responses = app.respond('george joined the channel', **{
        'Command': 'JOIN',
        'User': 'george'})
    assert responses == ["Beep BEEP! You received the following messages in #dummy-channel when you were offline.\nFrom repl_user 'I think I will be going.'\nFrom repl_user 'Are you going to the meeting?'"]


