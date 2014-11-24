FROM gwadeloop/botbotweb
MAINTAINER Yann Malet <yann.malet@gmail.com>

CMD manage.py run_plugins --settings=botbot.settings
