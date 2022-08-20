import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from google.oauth2 import service_account
import pandas_gbq
from google.cloud import bigquery
import os



credentials = service_account.Credentials.from_service_account_file('./key.json',)
os.environ['GOOGLE_APPLICATION_CREDENTIALS']='./key.json'
client = bigquery.Client()

productnpage = pandas_gbq.read_gbq(
f'SELECT * FROM `defect-detection-356414.for_logs.product` ',project_id='defect-detection-356414', credentials=credentials)
searchp=productnpage['product'].iloc[0]
pages=int(productnpage['pages'].iloc[0])
print('page number is',pages)


def scrape_using_product_name( searchp: str, pages:int):
    headers = {
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
    # 'Accept-Language': 'en-US, en;q=0.5'
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
    searchp=searchp
    search_query = searchp.replace(' ', '+')
    print(search_query)
    base_url = 'https://www.amazon.com/s?k={0}'.format(search_query)

    items = []
    pages=pages
    for i in range(pages):
        pages=pages+1
        print('Processing {0}...'.format(base_url + '&page={0}'.format(i)))
        response =requests.get(base_url + '&page={0}'.format(i), headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        results = soup.find_all('div', {'class': 's-result-item', 'data-component-type': 's-search-result'})

        for result in results:
            product_name = result.h2.text
            print(product_name)

            try:
                rating = result.find('i', {'class': 'a-icon'}).text
                print(rating)
                # rating_count = result.find_all('span', {'aria-label': True})[1].text
                # print(rating_count)
            except AttributeError:
                continue

            try:
                price1 = result.find('span', {'class': 'a-price-whole'}).text
                print(price1)
                price2 = result.find('span', {'class': 'a-price-fraction'}).text
                print(price2)
                price = float(price1 + price2)
                print(price)
                product_url = 'https://amazon.com' + result.h2.a['href']
                print(rating, product_url)
                items.append([product_name, rating, price, product_url])
            except AttributeError:
                continue
        sleep(1.5)
        
    df = pd.DataFrame(items, columns=['product', 'rating', 'price', 'product_url'])
    pandas_gbq.to_gbq(df, 'for_logs.product-search', project_id='defect-detection-356414', if_exists='replace', credentials=credentials)
    print(df)
    dml_statement = (f"delete FROM `defect-detection-356414.for_logs.product-search` where product_url like '%redirect%' or product_url like '%sspa%'")
    query_job = client.query(dml_statement)  # API request
    query_job.result()  # Waits for statement to finish
    return 'done'

scrape_using_product_name(searchp,pages)


