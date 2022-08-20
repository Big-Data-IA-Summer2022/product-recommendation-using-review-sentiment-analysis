import requests
from bs4 import BeautifulSoup
import pandas as pd


# url='https://www.amazon.com/product-reviews//B08C6K275N/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber=1'

HEADERS = ({'User-Agent':
			'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
			AppleWebKit/537.36 (KHTML, like Gecko) \
			Chrome/90.0.4430.212 Safari/537.36',
			'Accept-Language': 'en-US, en;q=0.5'})

df=[]
def getdata(url):
	r = requests.get(url, headers=HEADERS)
	return r.text

def html_code(url):
	htmldata = getdata(url)
	soup = BeautifulSoup(htmldata, 'html.parser')
	return (soup)

def cus_rev(soup):
	data_str = ""
	for item in soup.find_all("span", class_="a-size-base review-text review-text-content"):
		data_str = data_str + item.get_text()
	result = data_str.split("\n")
	return (result)

def get_reviews(url):
    url=url
    soup = html_code(url)
    rev_data = cus_rev(soup)
    rev_result = []
    df = pd.DataFrame()
    for i in rev_data:
        if i == "":
            pass
        else:
            rev_result.append(i)
    if bool(rev_result):
        df=pd.DataFrame(rev_result)
        return df
    if not rev_result:
        return df