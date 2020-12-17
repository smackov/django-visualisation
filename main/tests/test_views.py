from django.test import TestCase
from django.urls import reverse


class IndexTest(TestCase):
    "The test of index view"

    @classmethod
    def setUpTestData(cls):
        pass

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertAlmostEqual(response.status_code, 200)
        
    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        
        