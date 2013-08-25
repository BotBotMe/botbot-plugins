import requests
import urlparse

from ..base import BasePlugin
from .. import config
from ..decorators import listens_to_mentions


class Config(config.BaseConfig):
    url = config.Field(help_text="Jenkins URL")


class Plugin(BasePlugin):
    """
    Triggers builds on Jenkins.

    I can ask Jenkins to build jobs for you. Simply ask me:

        {{ nick }}: jenkins build <project_name>

    and I will forward the request to Jenkins.
    """

    config_class = Config

    @listens_to_mentions(ur'jenkins build (?P<job>[\w\-\_]+)')
    def build(self, line, job):
        """Trigger a build job on Jenkins"""
        auth, base_url = self.split_auth_and_url()
        base_job_url = base_url + '/job/{}'.format(job)
        # for handling parameterized builds later
        # url = base_job_url + '/buildWithParameters?{}'.format(params)
        url = base_job_url + '/build'
        resp = requests.post(url, auth=auth)
        if resp.status_code == 200:
            status_url = base_job_url + '/lastBuild/console'
            return "Build started for {0}.\n{1}".format(job, status_url)
        else:
            return "Error building {0}. Jenkins returned {1}.".format(
                job, resp.status_code)

    def split_auth_and_url(self):
        """Strip the auth bits out of the config URL if they exist"""
        base_url = self.config['url'].rstrip('/')
        parsed = urlparse.urlparse(base_url)
        if parsed.username and parsed.password:
            auth = (parsed.username, parsed.password)
        else:
            auth = None
        non_auth_url = parsed.scheme + '://' + parsed.hostname + parsed.path
        return auth, non_auth_url
