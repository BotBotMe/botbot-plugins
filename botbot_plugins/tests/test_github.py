import pytest
from mock import patch, call
import requests
from botbot_plugins.base import DummyApp
from botbot_plugins.plugins import github


class FakeResponse(object):
    """Dummy response from GitHub"""
    status_code = 200
    json = lambda x: {
        'title': 'import PIL',
        'html_url': 'https://github.com/lincolnloop/python-qrcode/issues/2'
    }


@pytest.fixture
def app():
    dummy_app = DummyApp(test_plugin=github.Plugin())
    dummy_app.set_config('github', {'organization': 'lincolnloop'})
    return dummy_app


def test_github(app):
    # patch requests.get so we don't need to make a real call to GitHub
    with patch.object(requests, 'get') as mock_get:
        mock_get.return_value = FakeResponse()
        responses = app.respond("I'm working on gh:python-qrcode#2 today")
        mock_get.assert_called_with(
            'https://api.github.com/repos/lincolnloop/python-qrcode/issues/2',
            auth=None)
        expected = ("import PIL: "
                    "https://github.com/lincolnloop/python-qrcode/issues/2")
        assert responses == [expected]


def test_github_multi(app):
    """Multiple issue lookup"""
    app.set_config('github', {'organization': 'gittip',
                              'repo': 'www.gittip.com'})
    with patch.object(requests, 'get') as mock_get:
        mock_get.return_value = FakeResponse()
        responses = app.respond("I'm working on gh1,2 today")
        expected_url = 'https://api.github.com/repos/gittip/www.gittip.com/issues/{}'
        mock_get.assert_has_calls([call(expected_url.format('1'), auth=None),
                                  call(expected_url.format('2'), auth=None)])
        assert len(responses) == 1
        assert len(responses[0].split(',')) == 2


def test_greediness(app):
    """Regression test for Github issue #8"""
    app.set_config('github', {'organization': 'gittip',
                              'repo': 'www.gittip.com'})
    with patch.object(requests, 'get') as mock_get:
        mock_get.return_value = FakeResponse()
        responses = app.respond("tough cookies")
        assert not mock_get.called, 'requests.get should not have been called'
        assert responses == []
        responses = app.respond("tough, cookies")
        assert not mock_get.called, 'requests.get should not have been called'
        assert responses == []
