from botbotme_plugins import base


def setup_function(function):
    # Monkey patch app and register plugin
    base.app = base.DummyApp(test_mode=True)
    import botbotme_plugins.plugins.github
    base.app.set_config('github', {
        'organization': 'lincolnloop'
    })


# FIXME `requests.get` needs to be mocked
def test_github():
    responses = base.app.respond("I'm working on gh:python-qrcode#2 today")
    expected = "import PIL: https://github.com/lincolnloop/python-qrcode/issues/2"
    assert responses == [expected]
