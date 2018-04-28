#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='botbot_plugins',
    version='1.0',
    description="Plugins and service integrations for BotBot.me",
    author="Lincoln Loop",
    author_email='info@lincolnloop.com',
    url='https://github.com/lincolnloop/botbot_plugins',
    packages=find_packages(),
    install_requires=(
        'pytest==3.5.1',
        'mock==2.0.0',
        'requests==2.18.4',
        'defusedxml==0.5.0',
        'fakeredis==0.10.2',
    ),
    scripts=['bin/botbot-shell'],
)
