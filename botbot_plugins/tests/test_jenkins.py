import pytest
from mock import patch, call
import requests
from botbot_plugins.base import DummyApp
from botbot_plugins.plugins import jenkins


class FakeResponse(object):
    """Dummy response from Jenkins"""
    def __init__(self, status_code=200):
        self.status_code = status_code


@pytest.fixture
def app():
    dummy_app = DummyApp(test_plugin=jenkins.Plugin())
    dummy_app.set_config('jenkins',
                         {'url': 'https://user:pw@jenkins.example.com/'})
    return dummy_app


def test_success_jenkins(app):
    # patch requests.post so we don't need to make a real call to Jenkins
    with patch.object(requests, 'post') as mock_post:
        mock_post.return_value = FakeResponse()
        responses = app.respond("@jenkins build myproj")
        assert responses == [
            '\n'.join(["Build started for myproj.",
            "https://jenkins.example.com/job/myproj/lastBuild/console"])
        ]


def test_fail_jenkins(app):
    # patch requests.post so we don't need to make a real call to Jenkins
    with patch.object(requests, 'post') as mock_post:
        mock_post.return_value = FakeResponse(status_code=405)
        responses = app.respond("@jenkins build myproj")
        assert responses == ["Error building myproj. Jenkins returned 405."]
