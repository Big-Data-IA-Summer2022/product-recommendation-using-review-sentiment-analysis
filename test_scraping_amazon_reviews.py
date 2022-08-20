import unittest
import requests 
from Scraping_Amazon_Reviews import best_reseller


class TestBestReseller(unittest.TestCase):
    def test_bestseller_url(self):
        url ="https://www.amazon.com/Best-Sellers/zgbs/ref=zg_bs_unv_ac_0_ac_1"
        HEADERS ={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
        response = requests.get(url, headers=HEADERS)
        if response.status_code > 500:
            assert "can't access the page"
        else:
            return 'success'
    def test_contentEsxists(self):
        data = len(best_reseller())
        if data is None:
            self.assertIsNone(data)
        else:
            'success'