from django.test import TestCase, SimpleTestCase
from django.shortcuts import redirect

# Create your tests here.
class First(SimpleTestCase):
    def view_test(self):
        url = redirect("polls:categories")
        resp = self.client.get(url)
        self.assertEquals(resp.status_code, 200)