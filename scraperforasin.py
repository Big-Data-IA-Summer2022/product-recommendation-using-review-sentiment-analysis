from types import NoneType
import pandas as pd
import selectorlib
import requests
from dateutil import parser as dateparser
import re
from google.oauth2 import service_account
import pandas_gbq
from google.cloud import bigquery
import os
import random
import time
from logfunc import logfunc

logfunc('script start','scraperforasin',200)

try:
    credentials = service_account.Credentials.from_service_account_file('./key.json',)
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']='./key.json'
    client = bigquery.Client()
except Exception as e:
    logfunc('Invalid credentials','scraperforasin',400)


try:
    productnpage = pandas_gbq.read_gbq(
    f'SELECT * FROM `defect-detection-356414.for_logs.product-asin` ',project_id='defect-detection-356414', credentials=credentials)
    print(productnpage)
    logfunc('read product-asin dataframe from BQ','scraperforasin',200)
except Exception as e:
    logfunc('unable to read product-asin dataframe from BQ','scraperforasin',300)


asin=productnpage['asin'].iloc[0]

print('asin is',asin)
y=int(productnpage['pages'].iloc[0])
print('page number is',y)



extractor = selectorlib.Extractor.from_yaml_file('selectors.yml')
print(extractor,'extractor')
def scrape(asin: str, y: int):
    if len(asin)!=10:
        logfunc('Invalid Asin','scraperforasin',300)
        return 'Invalid Asin'
    else:
        logfunc('valid Asin','scraperforasin',300)
        print('asin is valid')
    p=0
    n=0
    x=0
    df=pd.DataFrame()
    for i in range (y):
        x=x+1
        url=f"https://www.amazon.com/product-reviews/{asin}/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber={x}"
        headers = {
        'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        print("Downloading %s"%url)
        time.sleep(0.5 * random.random())
        r = requests.get(url, headers=headers)
        if r.status_code > 500:
            if "To discuss automated access to Amazon data please contact" in r.text:
                print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
            else:
                print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
            return None
        data = extractor.extract(r.text,base_url=url)
        if type(data['reviews']) == NoneType:
            return 'No reviews'
        print('extracted',data)
        reviews=[]
        for r in data['reviews']:
            r["product"] = data["product_title"]
            r['url'] = url
            r['rating'] = r['rating'].split(' out of')[0]
            date_posted = r['date'].split('on ')[-1]
            if r['images']:
                r['images'] = "\n".join(r['images'])
            r['date'] = dateparser.parse(date_posted).strftime('%d %b %Y')
            reviews.append(r)
        histogram = {}
        for h in data['histogram']:
            histogram[h['key']] = h['value']
        data['histogram'] = histogram
        data['average_rating'] = float(data['average_rating'].split(' out')[0])
        data['reviews'] = reviews
        data['number_of_reviews'] = str(data['number_of_reviews'].split('  customer')[0])
        df1 = pd.json_normalize(data['reviews'])
        df=df.append(df1,ignore_index=True)

    for i in df['content']:
        i = re.sub(r'[^a-zA-Z]', ' ', i)
        payload= {'text': i}
        url=f"https://damg7245-finalproject-sentiment-analysis-fol52rb4xq-ue.a.run.app/predict_sentiment?text={payload['text']}"
        response = requests.request("POST", url, params=payload)
        text=response.text
        if text=='"Positive"':
            p=p+1
        elif text=='"Negative"':
            n=n+1
    result=((p-n)/(p+n))*100
    print(p,n)
    print(result)
    df.drop("content", axis=1, inplace=True)
    df.drop("title", axis=1, inplace=True)
    df.drop("date", axis=1, inplace=True)
    df.drop("author", axis=1, inplace=True)
    df.drop("found_helpful", axis=1, inplace=True)
    df.drop("verified_purchase", axis=1, inplace=True)
    df['review_rating']=result
    df=df.head(1)
    print(df)
    
    try:
        pandas_gbq.to_gbq(df, 'for_logs.product-asin-ratings', project_id='defect-detection-356414', if_exists='replace', credentials=credentials)
        logfunc('Successfully populated table product-asin-ratings','scraperforasin',200)
    except Exception as e:
        logfunc('Unable to populate table product-asin-ratings','scraperforasin',500)

    return 'done'

scrape(asin,y)
