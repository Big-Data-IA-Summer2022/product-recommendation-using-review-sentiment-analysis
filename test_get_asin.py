import unittest
from asin_from_url import getasin

class TestGetASIN(unittest.TestCase):
    def test_success(self):
        actual = getasin('https://www.amazon.com/CamelBak-Water-Bottle-Airplane-Bandits-4/dp/B01LA75PTW/?_encoding=UTF8&pd_rd_w=veh54&content-id=amzn1.sym.8cf3b8ef-6a74-45dc-9f0d-6409eb523603&pf_rd_p=8cf3b8ef-6a74-45dc-9f0d-6409eb523603&pf_rd_r=H5YWJ4F2Z08KPS9VJMZE&pd_rd_wg=JUbZI&pd_rd_r=aa27872b-0ab7-40c1-9b79-70bfb7392b90&ref_=pd_gw_ci_mcx_mi')
        expected = 'B01LA75PTW'
        self.assertEqual(actual, expected)

    def test_exception(self):
        a = '123'
        with self.assertRaises(ValueError) as exception_context:
            getasin(a)
        self.assertEqual(
            str(exception_context.exception),
            "Invalid Input"
        )