from ..base import BasePlugin
from ..config import BaseConfig, Field
from ..decorators import listens_to_all


class MotivateConfig(BaseConfig):
    motivates_received = Field(
        required=False,
        help_text="If enabled, keeps track of how many "
                    "mentions a user receives",
        default=False
    )
    motivates_given = Field(
        required=False,
        help_text="If enabled, keeps track of how many "
                    "mentions a user receives",
        default=False
    )


class Plugin(BasePlugin):
    """
    Notifies people of the excellent work they are doing.

    Let me know who is doing good work:

        !m {{ nick }}

    And I will promptly notify them:

        You are doing good work {{ nick }}

    http://bangmotivate.appspot.com/
    """

    config_class = MotivateConfig

    @listens_to_all(ur'^\!m (?P<nick>.+?)$')
    def motivate(self, line, nick):
        if self.config['motivates_received'] and \
           self.config['motivates_given']:
                self.storage.store('{}-gtotal'.format(line.user))
                self.storage.set()

        return u"You're doing good work, {}!".format(nick)
