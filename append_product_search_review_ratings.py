import pandas as pd
from product_rating_final import get_rating_for_product
import pandas_gbq
from google.oauth2 import service_account
from google.cloud import bigquery
import os
from logfunc import logfunc

logfunc('script start','append_product_search_review_ratings',200)

credentials = service_account.Credentials.from_service_account_file('./key.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS']='./key.json'
client = bigquery.Client()

try:
    productnpage = pandas_gbq.read_gbq(
    f'SELECT * FROM `defect-detection-356414.for_logs.product` ',project_id='defect-detection-356414', credentials=credentials)
    pages=int(productnpage['pages'].iloc[0])
    pages=pages
    logfunc()
except Exception as e:
    logfunc('error in reading dataframe from bigquery product table','append_product_search_review_ratings',400)

try:

    df = pandas_gbq.read_gbq(
        'SELECT * FROM `defect-detection-356414.for_logs.product-search` ',project_id='defect-detection-356414', credentials=credentials)
    print(df)
    logfunc('success in reading product-search table','append_product_search_review_ratings',200)
except Exception as e:
    logfunc('error in reading dataframe from bigquery','append_product_search_review_ratings',400)


listforrating=[]
if len(df) !=0:
    for i in df['product_url']:
        d=get_rating_for_product(i,pages)
        print('d is', d)
        listforrating.append(d)
    logfunc('found ratings for all the products','append_product_search_review_ratings',200)
else:
    print('no products found to check')
    logfunc('no products found to check','append_product_search_review_ratings',400)
    raise SystemExit('No values in dataframe found to call sentiment API')
lfr=pd.Series(listforrating)
df['review_rating']=lfr.values
print(df)
try:
    pandas_gbq.to_gbq(df, 'for_logs.product-search-ratings', project_id='defect-detection-356414', if_exists='replace', credentials=credentials)
    logfunc('table populated with ratings','append_product_search_review_ratings',200)
except Exception as e:
    logfunc('table population failed for ratings','append_product_search_review_ratings',400)
logfunc('Script ends','append_product_search_review_ratings',200)
print('done')
