import unittest
from read_scraped import read_scraped ,read_scraped_with_ratings


class TestReadScraped(unittest.TestCase):
    def test_success(self):
        actual = read_scraped()
        expected = 'done'
        self.assertEqual(actual, expected)

class TestReadScrapedwithRating(unittest.TestCase):
    def test_success(self):
        actual = read_scraped_with_ratings()
        expected = 'done'
        self.assertEqual(actual, expected)