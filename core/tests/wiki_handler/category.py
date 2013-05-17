from django.utils import unittest
from core.handlers import wiki_handler
from wikipedia import Page

class Category_TestCase(unittest.TestCase):
    def setUp(self):
        self.w = wiki_handler()
        user_page = self.w.user.getUserPage()
        sandbox = Page(self.w.site, user_page.title()+'/Sandbox')
        self.test_pages = [ Page(self.w.site,sandbox.title()+p) for p in ('/test1','/test2') ]
        for p in self.test_pages:
            p.put('blablabla')

    def test_add_category(self):
        self.w.add_category(self.test_pages,'TEST CATEGORY')
        for p in self.test_pages:
            self.assertIn(':TEST CATEGORY]]',p.get() )

    def test_remove_category(self):
        self.w.remove_category(self.test_pages,'TEST CATEGORY')
        for p in self.test_pages:
            self.assertNotIn(':TEST CATEGORY]]',p.get() )
