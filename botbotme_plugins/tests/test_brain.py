from botbotme_plugins import base


def setup_function(function):
    # Monkey patch app and register plugin
    base.app = base.DummyApp(test_mode=True)
    import botbotme_plugins.plugins.brain


def test_remember():
    responses = base.app.respond(u"@shrug=¯\_(ツ)_/¯")
    assert responses == [u'I will remember "shrug" for you repl_user.']
    responses = base.app.respond(ur"@shrug ?")
    assert responses == [u"¯\_(ツ)_/¯"]


def test_recall():
    # TODO: understand why base.app.direct_messages_router is not set
    # {'brain': [(u'(?P<key>.+?)=\\s*(?P<value>.*)', <function remember at 0x1a2f7d0>), (u'(?P<key>.*)\\?', <function recall at 0x1a2f8c0>)]}
    assert {} != base.app.direct_messages_router

    base.app.storage[u'brain:shrug'] = '\xc3\x82\xc2\xaf\\_(\xc3\xa3\xc2\x83\xc2\x84)_/\xc3\x82\xc2\xaf'
    responses = base.app.respond(r"@shrug ?")
    assert responses == [u"¯\_(ツ)_/¯"]
