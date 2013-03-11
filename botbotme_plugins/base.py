from cmd import Cmd
import copy
import re
import sys


class BasePlugin(object):
    app = None
    config_class = None

    def __init__(self, *args, **kwargs):
        self.slug = self.__module__.split('.')[-1]

    @property
    def config(self):
        if hasattr(self, 'prod_config'):
            return self.prod_config
        if self.slug in self.app.plugin_configs:
            return self.app.plugin_configs[self.slug].fields
        return None

    def _unique_key(self, key):
        """A unique key for plugin, key combination"""
        return u'{0}:{1}'.format(self.slug, key.strip())

    def store(self, key, value):
        """Saves a key,value"""
        ukey = self._unique_key(key)
        self.app.storage[ukey] = unicode(value).encode('utf-8')

    def retrieve(self, key):
        """Retrieves the value for a key"""
        ukey = self._unique_key(key)
        value = self.app.storage.get(ukey, None)
        if value:
            value = unicode(value, 'utf-8')
        return value


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


REPL_INTRO = """
#########################
The BotBot.me plugin repl
#########################

Type a line to see how the plugins respond.
Prefix the line with `@` to send a direct message to the bot. Example:
    @ping

To configure a plugin, use `!!{plugin_name}:{field_name}={value}`. Example:
    !!github:organization=lincolnloop
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
        self.responses = []
        self.storage = {}
        self.messages_router = {}
        self.mentions_router = {}
        self.plugin_configs = {}
        if 'test_plugin' in kwargs:
            self.test_mode = True
            self.register(kwargs['test_plugin'])
            del(kwargs['test_plugin'])
        else:
            self.test_mode = False
        Cmd.__init__(self, *args, **kwargs)

    def register(self, plugin):
        """
        Introspects the Plugin class instance provided for methods
        that need to be registered with the internal app routers.
        """
        plugin.app = self
        for key in dir(plugin):
            attr = getattr(plugin, key)
            if (not key.startswith('__') and
                    getattr(attr, 'route_rule', None) and
                    attr.route_rule[0] in ('messages', 'mentions')):
                self.output('Route {}: {} ({}, {})'.format(attr.route_rule[0],
                                                           plugin.slug, key,
                                                           attr.route_rule[1]))
                getattr(self, attr.route_rule[0] + '_router').setdefault(
                    plugin.slug, []).append((attr.route_rule[1], attr))
                # Setup the plugin config
                if (plugin.config_class and
                        plugin.slug not in self.plugin_configs):
                    self.plugin_configs[plugin.slug] = plugin.config_class()

    def output(self, text):
        """Print text to stdout for repl. No-op for tests"""
        if not self.test_mode:
            print(text)

    def set_config(self, plugin_slug, fields_dict):
        """Manually set a plugin config. Used for testing"""
        self.plugin_configs[plugin_slug].fields.update(fields_dict)

    def respond(self, text):
        """Listens for incoming messages"""
        self.responses = []
        line = DummyLine({'text': text})
        self.dispatch(line)
        if self.test_mode:
            return self.responses

    # Cmd sends all text to the `default` method
    default = respond

    def do_EOF(self, arg):
        """Kill cmdloop on CTRL-d"""
        print "\nGoodbye"
        sys.exit()

    def do_shell(self, arg):
        """Handles lines prefaced with `!!`. Used to set config values"""
        if not arg.startswith('!'):
            return self.default(arg)
        try:
            plugin_slug, eq = arg[1:].split(':', 1)
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
        self.check_routes_for_matches(line, self.messages_router)

        if line.is_direct_message:
            self.check_routes_for_matches(line, self.mentions_router)

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
                        self.responses.append(response)
                        self.output('[o__o]: ' + response)

app = DummyApp()
