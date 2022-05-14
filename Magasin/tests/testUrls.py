from django.test import SimpleTestCase
from django.urls import reverse, resolve
from Magasin.views import *

class TestUrls(SimpleTestCase):

    def test_article_list(self):
        url = reverse('article_list')
        self.assertEquals(resolve(url).func, article_list)


    def test_commander(self):
        url = reverse('commander')
        self.assertEquals(resolve(url).func, commander)

    def test_stat(self):
        url = reverse('stat')
        self.assertEquals(resolve(url).func, statMag)


    def test_editcomm(self):
        url = reverse('editcomm', args="1")
        self.assertEquals(resolve(url).func, editcomm)

    def test_article_create(self):
        url = reverse('article_create')
        self.assertEquals(resolve(url).func, article_create)

    def test_article_update(self):
        url = reverse('article_update', args="1")
        self.assertEquals(resolve(url).func, article_update)


    def test_article_delete(self):
        url = reverse('article_delete', args="1")
        self.assertEquals(resolve(url).func, article_delete)


