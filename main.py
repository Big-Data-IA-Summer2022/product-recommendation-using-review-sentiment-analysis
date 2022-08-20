from keras.models import load_model
import os
import sys
import re
from keras_preprocessing.sequence import pad_sequences
import pickle
from fastapi import FastAPI
import uvicorn
from starlette.responses import RedirectResponse
import urllib
import pandas as pd
from google.oauth2 import service_account
import pandas_gbq
from google.cloud import bigquery



credentials = service_account.Credentials.from_service_account_file('./key.json',)
os.environ['GOOGLE_APPLICATION_CREDENTIALS']='./key.json'
client = bigquery.Client()


token_pickle='https://damg7245assignment.s3.amazonaws.com/tokenizer.pkl'
urllib.request.urlretrieve(token_pickle, 'file.pkl')
NON_ALPHANUM = re.compile(r'[\W]')
NON_ASCII = re.compile(r'[^a-z0-1\s]')
def normalize_texts(texts):
    normalized_texts = []
    for text in texts:
        lower = text.lower()
        no_punctuation = NON_ALPHANUM.sub(r' ', lower)
        no_non_ascii = NON_ASCII.sub(r'', no_punctuation)
        normalized_texts.append(no_non_ascii)
    return normalized_texts
MAX_LENGTH=255

app = FastAPI()

@app.post("/predict_sentiment")
async def prediction(text: str):
    text=[text]
    amazon_reviewscnn=os.path.join(sys.path[0], "amazon_reviewscnn.hdf5")
    model= load_model(amazon_reviewscnn)
    tokenizer = pickle.load(open('file.pkl',"rb"))
    #text=['I hate the product']
    text = normalize_texts(text)
    text = tokenizer.texts_to_sequences(text)
    text1 = pad_sequences(text, maxlen=MAX_LENGTH)
    pred = model.predict(text1)
    if pred >0.4:
        return 'Positive'
    else:
        return 'Negative'


@app.post("/scrape_product_using_product_search")
async def scrape_using_product_name( search_key: str, pages:int):
    items=[]
    searchp=search_key
    pages=pages
    items.append([searchp,pages])
    df=pd.DataFrame(items, columns=['product', 'pages'])
    print(df)
    pandas_gbq.to_gbq(df, 'for_logs.product', project_id='defect-detection-356414', if_exists='replace', credentials=credentials)
    return 'done'


@app.post("/scrape_product_using_product_url")
async def scrape_using_product_url( url: str, pages:int):
    items=[]
    searchp=url
    pages=pages
    items.append([searchp,pages])
    df=pd.DataFrame(items, columns=['url', 'pages'])
    print(df)
    pandas_gbq.to_gbq(df, 'for_logs.product-url', project_id='defect-detection-356414', if_exists='replace', credentials=credentials)
    return 'done'


@app.post("/scrape_product_using_product_asin")
async def scrape_using_product_asin( asin: str, pages:int):
    items=[]
    searchp=asin
    pages=pages
    items.append([searchp,pages])
    df=pd.DataFrame(items, columns=['asin', 'pages'])
    print(df)
    pandas_gbq.to_gbq(df, 'for_logs.product-asin', project_id='defect-detection-356414', if_exists='replace', credentials=credentials)
    return 'done'



@app.get("/")
async def index():
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    uvicorn.run(app, debug=True)
