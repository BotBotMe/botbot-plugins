import requests
from ..base import BasePlugin
from .. import config
from ..decorators import listens_to_all


class Config(config.BaseConfig):
    organization = config.Field(help_text="GitHub organization")
    repo = config.Field(required=False,
                        help_text="GitHub repository name")
    user = config.Field(
        required=False,
        help_text="GitHub username to connect to API (for private repos)")
    password = config.Field(
        required=False,
        help_text="GitHub password to connect to API (for private repos)")


class Plugin(BasePlugin):
    """
    Github issue lookup

    Looking for the url of an issue or a list of issue:

        gh#<issue_number>
        gh#<comma_separated_issue_numbers>

    Note: The lookup is limited to 5 issues.
    """
    url = "https://api.github.com/repos"
    config_class = Config

    @listens_to_all(ur'(?:.*)\b(?:GH|gh):(?P<repo>[\w\-\_]+)#?(?P<issues>\d+(?:,\d+)*)\b(?:.*)')
    def issue_lookup(self, line, repo, issues):
        """Lookup an specified repo issue"""
        # issues can be a list of issue separated by a comma
        issue_list = [i.strip() for i in issues.split(",")]
        response_list = []
        for issue in issue_list[:5]:
            api_url = "/".join([self.url, self.config['organization'],
                                repo, "issues", issue])
            response = requests.get(api_url, auth=self._get_auth())
            if response.status_code == 200:
                resp = u'{title}: {html_url}'.format(**response.json())
                response_list.append(resp)
            else:
                resp = u"Sorry I couldn't find issue #{0} in {1}/{2}".format(
                    issue, self.config['organization'], repo)
                response_list.append(resp)

        return ", ".join(response_list)


    @listens_to_all(ur'(?:.*)\b(?:GH|gh)#?(?P<issues>\d+(?:,\d+)*)\b(?:.*)')
    def project_issue_lookup(self, line, issues):
        """Lookup an issue for the default repo"""
        if not (self.config['organization'] and self.config['repo']):
            return
        # issues can be a list of issue separated by a comma
        issue_list = [i.strip() for i in issues.split(",")]
        response_list = []
        for issue in issue_list[:5]:
            api_url = "/".join([self.url, self.config['organization'],
                                self.config['repo'], "issues", issue])
            response = requests.get(api_url, auth=self._get_auth())
            if response.status_code == 200:
                resp = u'{title}: {html_url}'.format(**response.json())
                response_list.append(resp)
            else:
                resp = u"Sorry I couldn't find issue #{0} in {1}/{2}".format(
                    issue, self.config['organization'], self.config['repo'])
                response_list.append(resp)

        return ", ".join(response_list)

    def _get_auth(self):
        """Return user credentials if they are configured"""
        if self.config['user'] and self.config['password']:
            return (self.config['user'], self.config['password'])
        return None
