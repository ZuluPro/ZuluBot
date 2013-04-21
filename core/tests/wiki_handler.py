from django.utils import unittest
from wikipedia import Page
from core.handlers import wiki_handler
w = wiki_handler()

class get_page_TestCase(unittest.TestCase):

    def get_by_name(self):
        p = w.get_page('Accueil')
        self.assertIsInstance(p, Page, "Method 'get_page' doesn't return a Page object.")

    def get_by_name(self):
        pass
