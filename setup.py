#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='botbotme_plugins',
    version='1.0',
    description="Plugins and service integrations for BotBot.me",
    author="Lincoln Loop",
    author_email='info@lincolnloop.com',
    url='https://github.com/lincolnloop/botbotme_plugins',
    packages=find_packages(),
    install_requires=(
        'pytest==2.3.4',
        'mock==1.0.1',
        'requests==1.1.0',
        'defusedxml==0.4',
    ),
    scripts=['bin/botbotme_shell'],
)
