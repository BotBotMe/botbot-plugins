# -*- coding: utf-8 -*-
#import urllib
import requests
from defusedxml import ElementTree

from ..base import BasePlugin
from .. import config
from ..decorators import listens_to_mentions


class Config(config.BaseConfig):
    app_id = config.Field(help_text="Wolfram Alpha developer app ID")

class Plugin(BasePlugin):
    """
    Answers questions (via wolframalpha.com).

    I can recall almost any fact you wish. For example, if you would like to know
    the value of 500 US dollars in pounds sterling, you can ask:

        {{ nick }}: What is $500 in £?

    Can't find that silly little pound key on your keyboard? That's ok, you can
    use `GBP` instead.

    I can answer many questions that start with the words, `who`, `what`, `where`,
    `why`, and `when`. And yes, I even know:

        {{ nick }}: What is the air speed velocity of an unladen swallow?
    """
    config_class = Config
    url = "http://api.wolframalpha.com/v2/query?"

    @listens_to_mentions(ur'(W|w)(hat|here|ho|hy|hen) .*?\?')
    def search(self, line):
        message = line.text.encode('utf8')
        payload = {'input': message, 'appid': self.config['app_id']}

        response = requests.get(self.url, params=payload)

        try:
            tree = ElementTree.fromstring(response.content)
        except ElementTree.ParseError:
            return "Error parsing response from wolframalpha.com."

        if tree.attrib["success"] == "false":
            return u"I don't know"

        result = _gather_results(tree)

        try:
            return _answer(result, line)
        except (KeyError, IndexError):
            return "Error parsing response"


def _gather_results(tree):
    """Convert the XML tree into a map of pod types to tuples (title, value).
    """

    result = {}
    for pod in tree.findall('.//pod'):
        pod_type = pod.attrib['id']
        title = pod.attrib['title']

        val = None
        for plaintext in pod.findall('.//plaintext'):
            if plaintext.text:
                val = plaintext.text.replace(u"\n", u", ")

        if val:
            result[pod_type] = (title, val)

    return result


def _answer(result, line):
    """Answer the question as best as we can"""
    msgs = [u"Q: {}".format(result["Input"][1])]
    del result["Input"]

    for pod_type in ["Result", "Solution", "Derivative"]:
        if pod_type in result:
            msgs.append(u"A: {}".format(result[pod_type][1]))
            return '\n'.join(msgs)

    # We didn't find a specific answer - go into more detail

    for title, val in result.values():
        msgs.append(u"{}: {}".format(title, val))
        return '\n'.join(msgs)
