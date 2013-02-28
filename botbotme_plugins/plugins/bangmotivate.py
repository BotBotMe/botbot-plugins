from ..base import app

USER_DOCS = """
Notifies people of the excellent work they are doing.

Let me know who is doing good work:

    !m {{ nick }}

And I will promptly notify them:

    You are doing good work {{ nick }}

http://bangmotivate.appspot.com/
"""


@app.route(ur'^\!m (?P<nick>.+?)$', listens_to="all_messages")
def motivate(line, nick):
    return u"You're doing good work, {}!".format(nick)
