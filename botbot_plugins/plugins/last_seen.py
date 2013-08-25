import datetime
import time

from ..base import BasePlugin
from ..decorators import listens_to_mentions, listens_to_all


class Plugin(BasePlugin):
    """
    Tracks when a user was last seen online.

    I have an excellent memory and I never forget a nick.
    If you are curious to know when I last saw your colleague `MrTaubyPants`,
    ask me like so:

        {{ nick }}: seen MrTaubyPants?
    """
    @listens_to_all(ur'(.*)')
    def log_user_message(self, line):
        now = time.mktime(time.gmtime())
        self.store(line.user, u'{0}:{1}'.format(now, line.full_text))

    @listens_to_mentions(ur'seen\s*(?P<nick>[\w-]*)')
    def last_seen(self, line, nick):
        value = self.retrieve(nick)
        if value:
            timestamp, said = value.split(':', 1)
            date = datetime.datetime.fromtimestamp(float(timestamp))
            msg = u'Yes, I saw {0} {1}.\n'.format(nick, _timesince(date))
            msg += u'{0} said: "{1}"'.format(nick, said)
        else:
            msg = u"Sorry, I haven't seen {0}.".format(nick)
        return msg

# public domain via http://flask.pocoo.org/snippets/33/
def _timesince(dt, default="just now"):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """

    now = datetime.datetime.utcnow()
    diff = now - dt

    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )

    for period, singular, plural in periods:

        if period:
            return "%d %s ago" % (period, singular if period == 1 else plural)

    return default
