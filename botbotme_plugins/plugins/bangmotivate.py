from ..base import BasePlugin
from ..decorators import listens_to_all

USER_DOCS = """
Notifies people of the excellent work they are doing.

Let me know who is doing good work:

    !m {{ nick }}

And I will promptly notify them:

    You are doing good work {{ nick }}

http://bangmotivate.appspot.com/
"""


class Plugin(BasePlugin):

    @listens_to_all(ur'^\!m (?P<nick>.+?)$')
    def motivate(self, line, nick):
        return u"You're doing good work, {}!".format(nick)
