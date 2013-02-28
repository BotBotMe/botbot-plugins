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
    user = config.Field(required=False,
                        help_text="GitHub username to connect to API (for private repos)")
    password = config.Field(required=False,
                            help_text="GitHub password to connect to API (for private repos)")


URL = "https://api.github.com"

@app.route(ur'(?:.*)(?:GH|gh):(?P<repo>[\w\-\_]+)#?(?P<issues>[\d\s,]+)(?:.*)',
               listens_to="all_messages")
def issue_lookup(line, repo, issues):
    gh_config = line.plugin_config.fields
    # issues can be a list of issue separated by a comma
    issue_list = [i.strip() for i in issues.split(",")]
    response_list = []
    for issue in issue_list[:5]:
        api_url = "/".join([URL, "repos", gh_config['organization'],
                            repo, "issues", issue])
        if gh_config['user'] and gh_config['password']:
            auth = (gh_config['user'], gh_config['password'])
        else:
            auth = None
        response = requests.get(api_url, auth=auth)
        if response.status_code == 200:
            response_list.append(u'{title}: {html_url}'.format(**response.json))
        else:
            response_list.append(u"Sorry I couldn't find issue #{0} in {1}/{2}".format(issue, gh_config['organization'], repo))

    return ", ".join(response_list)

@app.route(ur'(?:.*)(?:GH|gh)#?(?P<issues>[\d\s,]+)(?:.*)',
               listens_to="all_messages")
def project_issue_lookup(line, issues):
    gh_config = line.plugin_config.fields
    if not (gh_config['organization'] and gh_config['repo']):
        return
    # issues can be a list of issue separated by a comma
    issue_list = [i.strip() for i in issues.split(",")]
    response_list = []
    for issue in issue_list[:5]:
        api_url = "/".join([URL, "repos", gh_config['organization'],
                            gh_config['repo'], "issues", issue])
        response = requests.get(api_url)
        if response.status_code == 200:
            response_list.append(u'{title}: {html_url}'.format(**response.json))
        else:
            response_list.append(u"Sorry I couldn't find issue #{0} in {1}/{2}".format(issue, gh_config['organization'], repo))

    return ", ".join(response_list)

