import pandas as pd
from product_rating_final import get_rating_for_product
import pandas_gbq
from google.oauth2 import service_account
from google.cloud import bigquery
import os

credentials = service_account.Credentials.from_service_account_file('./key.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS']='./key.json'
client = bigquery.Client()

productnpage = pandas_gbq.read_gbq(
f'SELECT * FROM `defect-detection-356414.for_logs.product` ',project_id='defect-detection-356414', credentials=credentials)
pages=int(productnpage['pages'].iloc[0])
pages=pages


df = pandas_gbq.read_gbq(
    'SELECT * FROM `defect-detection-356414.for_logs.product-search` ',project_id='defect-detection-356414', credentials=credentials)
print(df)
listforrating=[]
for i in df['product_url']:
    d=get_rating_for_product(i,pages)
    print('d is', d)
    listforrating.append(d)
lfr=pd.Series(listforrating)
df['review_rating']=lfr.values
print(df)
pandas_gbq.to_gbq(df, 'for_logs.product-search-ratings', project_id='defect-detection-356414', if_exists='replace', credentials=credentials)

print('done')