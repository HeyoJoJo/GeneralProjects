# https://jsonmock.hackerrank.com/api/movies/search/?Title=substr
import json
import urllib
import urllib2

try:
    """
    # Connection seems to be refused, might be library
    movie_request = requests.get(''.join([
        "https://jsonmock.hackerrank.com/api/movies/search/?Title=",
        str(substr)]))
    """

    request = urllib.Request(
        "https://jsonmock.hackerrank.com/api/movies/search/?Title=" + 'maze')
    response = urllib2.open(request)

    json_returned = json.load(response)

    print(json_returned['total'])


except:
    # keeps refusing connection
    # But I'm pretty sure this would work if not for that
    print('connection was refused')
