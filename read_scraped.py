import pandas as pd
from google.oauth2 import service_account
# from google.cloud import bigquery
import pandas_gbq
def read_scraped():
    csv=pd.read_csv('./AmazonBestSeller.csv')
    print(csv)
    credentials = service_account.Credentials.from_service_account_file('./key.json',)
    pandas_gbq.to_gbq(csv, 'for_logs.best-seller', project_id='defect-detection-356414', if_exists='replace', credentials=credentials)
    return 'done'
def read_scraped_with_ratings(text:str):
    csv=pd.read_csv(f'./AmazonBestSellerwithrating{text}.csv')
    credentials = service_account.Credentials.from_service_account_file('./key.json',)
    pandas_gbq.to_gbq(csv, f'for_logs.best-seller-with-ratings-{text}', project_id='defect-detection-356414', if_exists='replace', credentials=credentials)
    return 'done'
