import pandas as pd
from product_rating_final import get_rating_for_product
import pandas_gbq
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file('./key.json')
topics = pandas_gbq.read_gbq(
    f'SELECT TOPIC FROM `defect-detection-356414.for_logs.best-seller` group by topic ',project_id='defect-detection-356414', credentials=credentials)
topics=topics['TOPIC'].tolist()
print(topics)
for topic in topics:
    print('topic is',topic)
    df = pandas_gbq.read_gbq(
    f'SELECT * FROM `defect-detection-356414.for_logs.best-seller` where topic="{topic}" ',project_id='defect-detection-356414', credentials=credentials)
    print(df)
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
    df.to_csv(f'./AmazonBestSellerwithrating{topic}.csv', index=None)
    from read_scraped import read_scraped_with_ratings
    i=read_scraped_with_ratings(topic)
    print(i)