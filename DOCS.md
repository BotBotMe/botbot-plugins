## Plugin API Documentation

The easiest way to get started is to look at the existing plugins in `botbotme_plugins/plugins` as an example.

The `BasePlugin` class has the following public attributes:

* `config_class` (optional): A class inherited from `BaseConfig` defining any user-configurable fields, e.g. API keys. See `wolfram` or `github` for examples.
* `store(self, key, value)`: A method to store a simple key, value pair specific to the plugin. See `brain` and `last_seen` for examples.
* `retrieve(self, key)`: A method to retrieve a value for the given key. See `brain` and `last_seen` for examples.

### Parsing and responding to messages

Additional methods should be defined on your `Plugin` class that will listen and optionally respond to incoming messages. They are registered with the app using one of the following decorators from `botbotme_plugins.decorators`:

* `listens_to_mentions(regex)`: A method that should be called only when the bot's nick prefixes the message and that message matches the regex pattern. For example, `[o__o]: What time is it in Napier, New Zealand?`. The nick will be stripped prior to regex matching.
* `listens_to_all(regex)`: A method that should be called on any line that matches the regex pattern.

The method should accept a `line` object as its first argument and any named matches from the regex as keyword args. Any text returned by the method will be echoed back to the channel.

The `line` object has the following attributes:

* `user`: The nick of the user who wrote the message
* `text`: The text of the message (stripped of nick if addressed to the bot)
* `full_text`: The text of the message