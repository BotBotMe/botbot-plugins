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

@app.route(ur'(?P<key>.+?)=\s*(?P<value>.*)')
def remember(line, key, value):
    line.store(key, value)
    return u'I will remember "{0}" for you {1}.'.format(key, line.user)

@app.route(ur'(?P<key>.*)\?')
def recall(line, key):
    value = line.retrieve(key)
    if value:
        return value
