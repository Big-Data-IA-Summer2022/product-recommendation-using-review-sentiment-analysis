from sys import flags
import re
from logfunc import logfunc

logfunc('script start','asin from url',200)

def getasin(href):
    a='Invalid'
    asin = re.search(r'/[dg]p/([^/]+)', href, flags=re.IGNORECASE)
    try:
        asin=asin.group(1)
    except Exception as e:
        print('Invalid link unable to scrape asin')
        logfunc('invalid link','asin from url',400)
        return a
    logfunc('asin has been scraped','asin from url',200)
    print(asin)
    if asin != 'slredirect':
        logfunc('valid asin','asin from url',200)
        return asin
    else:
        logfunc('invalid asin','asin from url',400)
        return a

def getasin1(href):
    a='Invalid'
    asin = re.search(r'dp/([a-zA-Z]+([0-9]+[a-zA-Z]+)+)\?', href, flags=re.IGNORECASE)
    try:
        asin=asin.group(1)
    except Exception as e:
        print('Invalid link unable to scrape asin')
        logfunc('invalid link','asin from url',400)
        return a
    logfunc('asin has been scraped','asin from url',200)
    print(asin)
    if asin != 'slredirect':
        logfunc('valid asin','asin from url',200)
        return asin
    else:
        logfunc('invalid asin','asin from url',400)
        return a
