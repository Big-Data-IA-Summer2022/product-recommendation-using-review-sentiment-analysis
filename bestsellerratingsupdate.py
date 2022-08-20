import pandas as pd
from product_rating_final import get_rating_for_product
import pandas_gbq
from google.oauth2 import service_account
from logfunc import logfunc


logfunc('script start','bestsellerratingsupdate',200)
try:
    credentials = service_account.Credentials.from_service_account_file('./key.json')
except Exception as e:
    logfunc('credentials not found','bestsellerratingsupdate',400)


try:
    topics = pandas_gbq.read_gbq(
        f'SELECT TOPIC FROM `defect-detection-356414.for_logs.best-seller` group by topic ',project_id='defect-detection-356414', credentials=credentials)
    topics=topics['TOPIC'].tolist()
    print(topics)
    logfunc('dataframe has been read from bigquery','bestsellerratingsupdate',200)
except Exception as e:
    logfunc('Unable to read data from bigquery','bestsellerratingsupdate',400)
    raise SystemExit('No values read from bigquery so aborting')


for topic in topics:
    print('topic is',topic)
    try:
        df = pandas_gbq.read_gbq(
        f'SELECT * FROM `defect-detection-356414.for_logs.best-seller` where topic="{topic}" ',project_id='defect-detection-356414', credentials=credentials)
        print(df)
    except Exception as e:
        logfunc('Unable to read data from bigquery','bestsellerratingsupdate',400)

    listforrating=[]

    for i in df['Item_Url']:
        d=get_rating_for_product(i,1)
        print('d is', d)
        listforrating.append(d)

    lfr=pd.Series(listforrating)
    df['review_rating']=lfr.values
    print(df)
    topic=topic.replace('&','and')
    topic=topic.replace(',','')
    
    try:
        df.to_csv(f'./AmazonBestSellerwithrating{topic}.csv', index=None)
    except Exception as e:
        logfunc('Unable to create csv with rating locally','bestsellerratingsupdate',400)
    from read_scraped import read_scraped_with_ratings
    i=read_scraped_with_ratings(topic)
    print(i)
