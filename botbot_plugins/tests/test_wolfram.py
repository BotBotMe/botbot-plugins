import pytest
from mock import patch
import requests
from botbot_plugins.base import DummyApp
from botbot_plugins.plugins import wolfram


class FakeResponse(object):
    """Dummy response from GitHub"""
    status_code = 200
    content = """<?xml version='1.0' encoding='UTF-8'?>
<queryresult success='true'
    error='false'
    numpods='3'
    datatypes='City'
    timedout=''
    timedoutpods=''
    timing='1.48'
    parsetiming='0.775'
    parsetimedout='false'
    recalculate=''
    id='MSPa2221a5ca7e5e1i3gg90000046g17echc0h40615'
    host='http://www4b.wolframalpha.com'
    server='50'
    related='http://www4b.wolframalpha.com/api/v2/relatedQueries.jsp?id=MSPa2231a5ca7e5e1i3gg9000002df5d3ih5ie196f5&amp;s=50'
    version='2.6'>
<pod title='Input interpretation'
    scanner='Identity'
    id='Input'
    position='100'
    error='false'
    numsubpods='1'>
  <subpod title=''>
    <plaintext>convert 9:00 am PST | 11/03/2013 to UTC</plaintext>
      <img src='http://www4b.wolframalpha.com/Calculate/MSP/MSP2241a5ca7e5e1i3gg9000003bgehgb3bdf7bc1f?MSPStoreType=image/gif&amp;s=50'
        alt='convert 9:00 am PST | 11/03/2013 to UTC'
        title='convert 9:00 am PST | 11/03/2013 to UTC'
        width='271'
        height='18' />
  </subpod>
</pod>
<pod title='Result'
     scanner='Identity'
     id='Result'
     position='200'
     error='false'
     numsubpods='1'
     primary='true'>
  <subpod title='' primary='true'>
    <plaintext>4:00:00 pm GMT  |  Monday, March 11, 2013</plaintext>
    <img src='http://www4b.wolframalpha.com/Calculate/MSP/MSP2251a5ca7e5e1i3gg9000001a455cb2f0e511fc?MSPStoreType=image/gif&amp;s=50'
      alt='4:00:00 pm GMT  |  Monday, March 11, 2013'
      title='4:00:00 pm GMT  |  Monday, March 11, 2013'
      width='303'
      height='18' />
  </subpod>
</pod>
<pod title='Time difference from now (9:37:53 am GMT)'
     scanner='Date'
     id='TimeDifferenceFromNow (time)'
     position='300'
     error='false'
     numsubpods='1'>
  <subpod title=''>
    <plaintext>6 hours 22 minutes 6 seconds in the future</plaintext>
    <img src='http://www4b.wolframalpha.com/Calculate/MSP/MSP2261a5ca7e5e1i3gg9000003068g38g4a45bbi6?MSPStoreType=image/gif&amp;s=50'
        alt='6 hours 22 minutes 6 seconds in the future'
        title='6 hours 22 minutes 6 seconds in the future'
        width='272'
        height='18' />
  </subpod>
</pod>
<sources count='2'>
<source url='http://www.wolframalpha.com/sources/CityDataSourceInformationNotes.html'
text='City data' />
<source url='http://www.wolframalpha.com/sources/TimeZoneDataSourceInformationNotes.html'
    text='Time zone data' />
</sources>
</queryresult>
"""


@pytest.fixture
def app():
    app = DummyApp(test_plugin=wolfram.Plugin())
    app.set_config('wolfram', {"app_id": "secret-appid"})
    return app


def test_github(app):
    # patch requests.get so we don't need to make a real call to GitHub
    with patch.object(requests, 'get') as mock_get:
        mock_get.return_value = FakeResponse()
        responses = app.respond("@What is 9 am PST in UTC ?")
        mock_get.assert_called_with('http://api.wolframalpha.com/v2/query?',
                                    params={
                                        'input': 'What is 9 am PST in UTC ?',
                                        'appid': 'secret-appid'})
        expected = u'Q: convert 9:00 am PST | 11/03/2013 to UTC\nA: 4:00:00 pm GMT  |  Monday, March 11, 2013'
        assert responses == [expected]
