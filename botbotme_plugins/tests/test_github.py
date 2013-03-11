import pytest
from mock import patch
import requests
from botbotme_plugins.base import DummyApp
from botbotme_plugins.plugins import github


class FakeResponse(object):
    """Dummy response from GitHub"""
    status_code = 200
    json = lambda x: {
        'title': 'import PIL',
        'html_url': 'https://github.com/lincolnloop/python-qrcode/issues/2'
    }


@pytest.fixture
def app():
    app = DummyApp(test_plugin=github.Plugin())
    app.set_config('github', {'organization': 'lincolnloop'})
    return app


def test_github(app):
    # patch requests.get so we don't need to make a real call to GitHub
    with patch.object(requests, 'get') as mock_get:
        mock_get.return_value = FakeResponse()
        responses = app.respond("I'm working on gh:python-qrcode#2 today")
        expected_url = 'https://api.github.com/repos/lincolnloop/python-qrcode/issues/2'
        mock_get.assert_called_with(expected_url, auth=None)
        expected = "import PIL: https://github.com/lincolnloop/python-qrcode/issues/2"
        assert responses == [expected]
