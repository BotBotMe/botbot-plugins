import pytest
from botbotme_plugins.base import DummyApp
from botbotme_plugins.plugins import github


@pytest.fixture
def app():
    app = DummyApp(test_plugin=github.Plugin())
    app.set_config('github', {'organization': 'lincolnloop'})
    return app


# FIXME `requests.get` needs to be mocked
def test_github(app):
    responses = app.respond("I'm working on gh:python-qrcode#2 today")
    expected = "import PIL: https://github.com/lincolnloop/python-qrcode/issues/2"
    assert responses == [expected]
