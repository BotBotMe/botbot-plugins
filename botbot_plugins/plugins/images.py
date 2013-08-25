import re
import random
from urllib import urlencode

import requests

from ..base import BasePlugin
from ..decorators import listens_to_mentions


class Plugin(BasePlugin):
    """
    Image lookup (via Google Images)

    Looking for a link to an image? Allow me to find it for you. If you say:

        {{ nick }}: image me cats

    I'll send you a link to an image brimming with cats (that's my job).
    Would you prefer to have a picture of cats that is animated?
    I'll do my best to find one when you say:

        {{ nick }}: animate me cats

    And finally, if you are feeling downright silly, well I will put a mustache
    on any image you request (via mustachify.me). I can do this in one of two ways:

        {{ nick }}: mustache me the queen of england

    Alternatively, if you already have an image of the Queen of England that is
    perfect for a good mustaching, you can give me the link:

        {{ nick }}: mustache me http://example.com/queen_of_england.jpg
    """
    @listens_to_mentions(ur'(image|img)( me)? (?P<image>.*)')
    def respond_to_image(self, line, image):
        url = image_me(image)
        return url


    @listens_to_mentions(ur'(animate)( me)? (?P<image>.*)')
    def respond_to_animate(self, line, image):
        url = image_me(image, animated=True)
        return url


    @listens_to_mentions(ur'(?:mo?u)?sta(?:s|c)he?(?: me)? (?P<image>.*)')
    def respond_to_mustache(self, line, image):
        mustache = random.choice([0, 1, 2])
        mustachify = "http://mustachify.me/{mustache}?src={url}"
        if re.match(r'^https?:\/\/', image, re.IGNORECASE):
            url = image
        else:
            url = image_me(image)
        return mustachify.format(mustache=mustache, url=url)


def image_me(query, animated=False):
    query = query.encode("utf8")
    query_dict = {'v': '1.0', 'rsz': '8', 'q': query, 'safe': 'active'}
    if animated:
        query_dict['as_filetype'] = 'gif'
    url = 'http://ajax.googleapis.com/ajax/services/search/images?{0}'.format(
        urlencode(query_dict))
    response = requests.get(url)
    images = response.json()['responseData']['results']
    if len(images) > 0:
        image = images[0]
        return image['unescapedUrl'] + '#.png'
