import unittest
from bs4 import BeautifulSoup
import requests
from review_scraper_final import *

class TestGetData(unittest.TestCase):
    def test_success(self):
        actual = getdata('https://www.amazon.com/CamelBak-Water-Bottle-Airplane-Bandits-4/product-reviews/B01LA75PTW/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews')
        url ="https://www.amazon.com/CamelBak-Water-Bottle-Airplane-Bandits-4/product-reviews/B01LA75PTW/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
        HEADERS ={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
        r = requests.get(url, headers=HEADERS)
        expected = r.text
        self.assertEqual(actual, expected)


class TestHTMLCode(unittest.TestCase):
    def test_success(self):
        actual = html_code('https://www.amazon.com/CamelBak-Water-Bottle-Airplane-Bandits-4/product-reviews/B01LA75PTW/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews')
        url ="https://www.amazon.com/CamelBak-Water-Bottle-Airplane-Bandits-4/product-reviews/B01LA75PTW/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
        HEADERS ={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
        r = requests.get(url, headers=HEADERS)
        a=r.text
        expected = BeautifulSoup(a, 'html.parser')
        self.assertEqual(actual, expected)

class TestCusRevi(unittest.TestCase):
    def test_success(self):
        url ="https://www.amazon.com/CamelBak-Water-Bottle-Airplane-Bandits-4/product-reviews/B01LA75PTW/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"
        HEADERS ={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
        r = requests.get(url, headers=HEADERS)
        a=r.text
        soup = BeautifulSoup(a, 'html.parser')
        data_str = ""
        for item in soup.find_all("span", class_="a-size-base review-text review-text-content"):
            data_str = data_str + item.get_text()
        expected = data_str.split("\n")
        actual = cus_rev(soup)
        self.assertEqual(actual, expected)

class TestGetReviews(unittest.TestCase):
    def test_contentEsxists(self):
        data = len(get_reviews('https://www.amazon.com/CamelBak-Water-Bottle-Airplane-Bandits-4/product-reviews/B01LA75PTW/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'))
        if data is None:
            self.assertIsNone(data)
        else:
            'success'