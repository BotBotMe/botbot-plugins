from ..base import BasePlugin
from ..decorators import listens_to_mentions


class Plugin(BasePlugin):
    """
    Remembers and recalls arbitrary information.

    To have me remember something for you, ask me in this format:

        {{ nick }}: thing you remember = thing I need to remember

    When you want me to recall the information, ask me in this format:

        {{ nick }}: thing you remember?

    I will prompty respond to your request with:

        thing I need to remember
    """

    @listens_to_mentions(ur'(?P<key>.+?)=\s*(?P<value>.*)')
    def remember(self, line, key, value):
        self.store(key, value)
        return u'I will remember "{0}" for you {1}.'.format(key, line.user)

    @listens_to_mentions(ur'(?P<key>.*)\?')
    def recall(self, line, key):
        value = self.retrieve(key)
        if value:
            return value
