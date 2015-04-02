from django.test import TestCase
from django.core.urlresolvers import reverse
from bus_stop.views import nearest_buses


class BusStopTest(TestCase):

    ####################
    # helper functions #
    ####################

    def get_nearest_x(self, x):
        """set up 3 buses and find the x nearest"""
        bus1 = dict(latitude=10, longitude=-10)
        bus2 = dict(latitude=-20, longitude=-20)
        bus3 = dict(latitude=100, longitude=100)

        buses = [bus1, bus2, bus3]
        my_lat = 10.0
        my_lng = 10.0

        return nearest_buses(buses, my_lat, my_lng, x), bus1, bus2, bus3

    def test_0_nearest_buses(self):
        """ensure that 0 nearest buses are found"""
        nearest, b1, b2, b3 = self.get_nearest_x(0)
        self.assertEquals(nearest, [])

    def test_1_nearest_buses(self):
        """ensure that 1 nearest bus is found"""
        nearest, b1, b2, b3 = self.get_nearest_x(1)
        self.assertEquals(nearest, [b1])

    def test_2_nearest_buses(self):
        """ensure that the 2 nearest buses are found"""
        nearest, b1, b2, b3 = self.get_nearest_x(2)
        self.assertEquals(nearest, [b1, b2])

    ##########
    # models #
    ##########

    ########################
    # views (uses reverse) #
    ########################

    def test_stops_load(self):
        """ensure that the stops page loads"""
        response = self.client.get(reverse("stops"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Deans South', response.content)

    def test_live_buses_load(self):
        """ensure that the live buses page loads"""
        response = self.client.get(reverse("live_buses"), data=dict(lat='55.9443730', lng='-3.1868930'))
        self.assertEqual(response.status_code, 200)

    #########
    # forms #
    #########



