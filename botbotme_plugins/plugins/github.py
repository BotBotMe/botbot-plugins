import requests
from ..base import app
from .. import config


USER_DOCS = """
Github issue lookup

Looking for the url of an issue or a list of issue:

    gh#<issue_number>
    gh#<comma_separated_issue_numbers>

Note: The lookup is limited to 5 issues.
"""


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


URL = "https://api.github.com/repos"


@app.route(ur'(?:.*)(?:GH|gh):(?P<repo>[\w\-\_]+)#?(?P<issues>[\d\s,]+)(?:.*)',
           listens_to="all_messages")
def issue_lookup(line, repo, issues):
    """Lookup an specified repo issue"""
    gh_config = line.plugin_config.fields
    # issues can be a list of issue separated by a comma
    issue_list = [i.strip() for i in issues.split(",")]
    response_list = []
    for issue in issue_list[:5]:
        api_url = "/".join([URL, gh_config['organization'],
                            repo, "issues", issue])
        response = requests.get(api_url, auth=_get_auth(gh_config))
        if response.status_code == 200:
            resp = u'{title}: {html_url}'.format(**response.json())
            response_list.append(resp)
        else:
            resp = u"Sorry I couldn't find issue #{0} in {1}/{2}".format(
                issue, gh_config['organization'], repo)
            response_list.append(resp)

    return ", ".join(response_list)


@app.route(ur'(?:.*)(?:GH|gh)#?(?P<issues>[\d\s,]+)(?:.*)',
           listens_to="all_messages")
def project_issue_lookup(line, issues):
    """Lookup an issue for the default repo"""
    gh_config = line.plugin_config.fields
    if not (gh_config['organization'] and gh_config['repo']):
        return
    # issues can be a list of issue separated by a comma
    issue_list = [i.strip() for i in issues.split(",")]
    response_list = []
    for issue in issue_list[:5]:
        api_url = "/".join([URL, gh_config['organization'],
                            gh_config['repo'], "issues", issue])
        response = requests.get(api_url, auth=_get_auth(gh_config))
        if response.status_code == 200:
            resp = u'{title}: {html_url}'.format(**response.json())
            response_list.append(resp)
        else:
            resp = u"Sorry I couldn't find issue #{0} in {1}/{2}".format(
                issue, gh_config['organization'], gh_config['repo'])
            response_list.append(resp)

    return ", ".join(response_list)

def _get_auth(gh_config):
    """Return user credentials if they are configured"""
    if gh_config['user'] and gh_config['password']:
        return (gh_config['user'], gh_config['password'])
    return None
