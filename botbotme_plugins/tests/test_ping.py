from botbotme_plugins import base


def setup_function(function):
    # Monkey patch app and register plugin
    base.app = base.DummyApp(test_mode=True)
    import botbotme_plugins.plugins.ping


def test_ping():
    responses = base.app.respond("@ping")
    assert responses == ["Are you in need of my services, repl_user?"]


def test_noping():
    responses = base.app.respond("shouldn't ping === false?")
    assert len(responses) == 0
