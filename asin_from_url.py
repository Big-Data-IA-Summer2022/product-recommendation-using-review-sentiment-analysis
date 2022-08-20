
from sys import flags
import requests
import re

###Amazon URL
def getasin(href):
    a='Invalid'
    asin = re.search(r'/[dg]p/([^/]+)', href, flags=re.IGNORECASE)
    asin=asin.group(1)
    print(asin)
    if asin != 'slredirect':
        return asin
    else:
        return a

def getasin1(href):
    a='Invalid'
    asin = re.search(r'dp/([a-zA-Z]+([0-9]+[a-zA-Z]+)+)\?', href, flags=re.IGNORECASE)
    asin=asin.group(1)
    print(asin)
    if asin != 'slredirect':
        return asin
    else:
        return a