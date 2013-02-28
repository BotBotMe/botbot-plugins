from cmd import Cmd
import copy
import re
import sys


class DummyLine(object):
    """
    All the methods and data necessary for a plugin to act on a line
    """
    def __init__(self, packet, slug=''):
        self.text = packet['text']
        self.full_text = packet['text']
        self.user = 'repl_user'
        self.plugin_slug = ''
        self.is_direct_message = self.check_direct_message()

    def check_direct_message(self):
        """Are you addressing the bot?"""
        if self.text.startswith('@'):
            self.text = self.text[1:]
            return True
        return False

    def _unique_key(self, key):
        """A unique key for plugin, key combination"""
        return u'{0}:{1}'.format(self.plugin_slug, key.strip())

    def store(self, key, value):
        """Saves a key,value"""
        ukey = self._unique_key(key)
        app.storage[ukey] = unicode(value).encode('utf-8')

    def retrieve(self, key):
        """Retrieves the value for a key"""
        ukey = self._unique_key(key)
        value = app.storage.get(ukey, None)
        if value:
            value = unicode(value, 'utf-8')
        return value

REPL_INTRO = """
#########################
The BotBot.me plugin repl
#########################

Type a line to see how the plugins respond.
Prefix the line with `@` to send a direct message to the bot. Example:
    @ping

To configure a plugin, use `!{plugin_name}:{field_name}={value}`. Example:
    !github:organization=lincolnloop
"""


class DummyApp(Cmd):
    """
    Registration and routing for plugins
    """
    listener_types = ('all_messages', 'direct_messages')
    prompt = '(repl_user) '
    intro = REPL_INTRO
    use_raw_input = False

    def __init__(self, *args, **kwargs):
        # Cmd is an old-style class, super doesn't work
        # super(DummyApp, self).__init__(*args, **kwargs)
        Cmd.__init__(self, *args, **kwargs)
        self.storage = {}
        self.all_messages_router = {}
        self.direct_messages_router = {}
        self.plugin_configs = {}

    def route(self, rule, listens_to='direct_messages'):
        """Decorator to add function and rule to routing table"""
        if not listens_to in self.listener_types:
            raise AttributeError('Invalid route listens_to. '
                                 'Options are: {}'.format(self.listener_types))

        def decorator(func):
            # gets the name of the python module containing the function
            slug = func.__module__.split('.')[-1]
            print(u"Adding route: {0} -> {1}".format(func.__name__, rule))
            router = getattr(self, listens_to + '_router')
            router.setdefault(slug, []).append((rule, func))
            module = sys.modules[func.__module__]
            if hasattr(module, 'Config') and slug not in self.plugin_configs:
                self.plugin_configs[slug] = module.Config()
            return func
        return decorator

    def default(self, text):
        """Listens for incoming messages"""
        line = DummyLine({'text': text})
        self.dispatch(line)

    def do_EOF(self, arg):
        """Kill cmdloop on CTRL-d"""
        print "\nGoodbye"
        sys.exit()

    def do_shell(self, arg):
        """Handles lines prefaced with `!`. Used to set config values"""
        try:
            plugin_slug, eq = arg.split(':', 1)
            field, value = eq.split('=', 1)
        except ValueError:
            print("Bad config format. {plugin_slug}:{field_name}={value}")
            return
        if plugin_slug not in self.plugin_configs:
            print('No config defined for "{0}"'.format(plugin_slug))
            return
        if field not in self.plugin_configs[plugin_slug].fields:
            print('Field "{0}" is not defined for "{1}"'.format(field,
                                                               plugin_slug))
            return
        self.plugin_configs[plugin_slug].fields[field] = value
        print('Config saved.')


    def dispatch(self, line):
        """Given a line, dispatch it to the right function(s)"""
        self.check_routes_for_matches(line, self.all_messages_router)

        if line.is_direct_message:
            self.check_routes_for_matches(line, self.direct_messages_router)

    def check_routes_for_matches(self, line, router):
        """Checks if line matches the routes' rules and calls functions"""
        for slug, route_list in router.items():
            for rule, func in route_list:
                match = re.match(rule, line.text, re.IGNORECASE)
                if match:
                    # attach the correct plugin slug to the line obj
                    # required to make a unique key for the storage
                    plugin_line = copy.deepcopy(line)
                    plugin_line.plugin_slug = slug
                    if (slug in self.plugin_configs and
                            self.plugin_configs[slug].is_valid()):
                        plugin_line.plugin_config = self.plugin_configs[slug]
                    response = func(plugin_line, **match.groupdict())
                    if response:
                        print('[o__o]: ' + response)

app = DummyApp()
