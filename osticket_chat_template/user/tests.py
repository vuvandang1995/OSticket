from django.test import SimpleTestCase, Client


class TestUserViews(SimpleTestCase):
   def test_index(self):
       self.client = Client()
       response = self.client.get('/')
       self.assertEqual(response.status_code, 200)