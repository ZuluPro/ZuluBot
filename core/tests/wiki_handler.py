from django.utils import unittest
from django.conf import settings
from wikipedia import Page
from core.handlers import wiki_handler
w = wiki_handler()

class add_category_TestCase(unittest.TestCase):

    def setUp(self):
        self.base_text = w.get_page().get()

    def tearDown(self):
        pass

    def get_by_name(self):
        p = w.get_page('Accueil')
        self.assertIsInstance(p, Page, "Method 'get_page' doesn't return a Page object.")

    def get_by_name(self):
        pass
