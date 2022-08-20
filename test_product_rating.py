import unittest
from product_rating_final import get_rating_for_product



class TestGetProductReviewRating(unittest.TestCase):
    def test_exception(self):
        a='123'
        with self.assertRaises(ValueError) as exception_context:
            get_rating_for_product(a,1)
        self.assertEqual(
            str(exception_context.exception),
            "Invalid Input"
        )