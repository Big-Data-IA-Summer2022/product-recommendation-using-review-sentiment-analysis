import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from google.oauth2 import service_account
import pandas_gbq
from google.cloud import bigquery
import os
from logfunc import logfunc


logfunc('script start','product_name_scrape',200)
try:
    credentials = service_account.Credentials.from_service_account_file('./key.json',)
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']='./key.json'
    client = bigquery.Client()
    logfunc('valid credentials','product_name_scrape',400)
except Exception as e:
    logfunc('Invalid or unable to find credentials','product_name_scrape',400)

try:
    productnpage = pandas_gbq.read_gbq(
    f'SELECT * FROM `defect-detection-356414.for_logs.product` ',project_id='defect-detection-356414', credentials=credentials)
    searchp=productnpage['product'].iloc[0]
    pages=int(productnpage['pages'].iloc[0])
    print('page number is',pages)
except Exception as e:
    logfunc('Unable to query bigquery','product_name_scrape',400)



def scrape_using_product_name( searchp: str, pages:int):
    headers = {
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
    # 'Accept-Language': 'en-US, en;q=0.5'
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
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',}
    searchp=searchp
    print(searchp)
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
        
        try:
            results = soup.find_all('div', {'class': 's-result-item', 'data-component-type': 's-search-result'})
            logfunc('site has been scraped','product_name_scrape',200)
        except Exception as e:
            logfunc('site was not scraped through bs4','product_name_scrape',400)

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
                price = price1
                print(price)
                product_url = 'https://amazon.com' + result.h2.a['href']
                print(rating, product_url)
                items.append([product_name, rating, price, product_url])
            except AttributeError:
                continue
        sleep(1.5)
        
    df = pd.DataFrame(items, columns=['product', 'rating', 'price', 'product_url'])
    try:
        pandas_gbq.to_gbq(df, 'for_logs.product-search', project_id='defect-detection-356414', if_exists='replace', credentials=credentials)
        logfunc('product-search table populated','product_name_scrape',200)
    except Exception as e:
        logfunc('product-search table unable populated','product_name_scrape',500)

    print(df)
    dml_statement = (f"delete FROM `defect-detection-356414.for_logs.product-search` where product_url like '%redirect%' or product_url like '%sspa%'")
    query_job = client.query(dml_statement)  # API request
    query_job.result()  # Waits for statement to finish
    return 'done'

scrape_using_product_name(searchp,pages)


