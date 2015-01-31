from django.test import TestCase
from django.core.urlresolvers import reverse


class TransportAPITests(TestCase):

    def test_stops_load(self):
        """ensure that the stops page loads"""
        response = self.client.get(reverse("stops"))
        self.assertEqual(response.status_code, 200)


