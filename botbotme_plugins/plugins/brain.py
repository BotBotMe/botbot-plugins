from ..base import app

USER_DOCS = """
Remembers and recalls arbitrary information.

To have me remember something for you, ask me in this format:

    {{ nick }}: thing you remember = thing I need to remember

When you want me to recall the information, ask me in this format:

    {{ nick }}: thing you remember?

I will prompty respond to your request with:

    thing I need to remember
"""


class Rule(object):
    def __init__(self, pattern, action):
        self.pattern = pattern
        self.action = action


class Plugin(object):
    def __init__(self, slug, rules, listens_to="direct_messages"):
        self.slug = slug
        self.rules = rules
        self.listens_to = listens_to


def remember_action(line, key, value):
    line.store(key, value)
    return u'I will remember "{0}" for you {1}.'.format(key, line.user)


def recall_action(line, key):
    value = line.retrieve(key)
    if value:
        return value


brain = Plugin("brain",
               rules=[Rule(ur'(?P<key>.+?)=\s*(?P<value>.*)', remember_action),
                      Rule(ur'(?P<key>.*)\?', recall_action)])
