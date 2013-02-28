# BotBot.me Plugins

To get started:

```
$ pip install -e git+git@github.com:lincolnloop/botbotme-plugins.git#egg=botbotme-plugins
$ botbotme_shell
```

Pass a comma-separated list of modules to run a subset of the plugins:

```
$ botbotme_shell brain,images
```

## Tests

```
py.test botbotme_plugins
```

Fork and add new plugins to the `plugins` directory. Have fun!
