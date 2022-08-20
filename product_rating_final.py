from review_scraper import *
from asin_from_url import *
import requests
import re
import pandas as pd

def get_rating_for_product(url: str,y: int):
    if len(getasin(url))==10:
        asin=(getasin(url))
    elif len(getasin1(url))==10:
        asin=getasin1(url)
    print(asin)
    p=0
    n=0
    brokenapi=0
    for x in range(y):
        x=x+1
        url=f"https://www.amazon.com/product-reviews/{asin}/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber={x}"
        print("Downloading %s"%url)
        df=get_reviews(url)
        print(df)
        if df.empty:
            pass
        else:
            for i in df[0]:
                i = re.sub(r'[^a-zA-Z]', ' ', i)
                payload= {'text': i}
                url=f"https://damg7245-finalproject-sentiment-analysis-fol52rb4xq-ue.a.run.app/predict_sentiment?text={payload['text']}"
                response = requests.request("POST", url, params=payload)
                text=response.text
                if text=='"Positive"':
                    p=p+1
                elif text=='"Negative"':
                    n=n+1
                else:
                    brokenapi+=1
    print(p,n) 
    if p+n!=0:
        result=((p-n)/(p+n))*100
        print(result)
    elif p+n==0:
        result='No reviews'
        print('No reviews')
    return result

