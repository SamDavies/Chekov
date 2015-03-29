from collections import namedtuple
from django.test import TestCase
from django.core.urlresolvers import reverse
from bus_stop.views import nearest_buses


class BusStopTest(TestCase):

    ####################
    # helper functions #
    ####################

    def test_0_nearest_buses(self):
        LiveBus = namedtuple("LiveBus", "latitude longitude")
        bus1 = LiveBus(10, -10)
        bus2 = LiveBus(-20, -20)
        bus3 = LiveBus(100, 100)

        buses = [bus1, bus2, bus3]
        my_lat = 10.0
        my_lng = 10.0

        nearest = nearest_buses(buses, my_lat, my_lng, 0)
        self.assertEquals(nearest, [])

    def test_1_nearest_buses(self):
        LiveBus = namedtuple("LiveBus", "latitude longitude")
        bus1 = LiveBus(10, -10)
        bus2 = LiveBus(-20, -20)
        bus3 = LiveBus(100, 100)

        buses = [bus1, bus2, bus3]
        my_lat = 10.0
        my_lng = 10.0

        nearest = nearest_buses(buses, my_lat, my_lng, 1)
        self.assertEquals(nearest, [bus1])

    def test_2_nearest_buses(self):
        LiveBus = namedtuple("LiveBus", "latitude longitude")
        bus1 = LiveBus(10, -10)
        bus2 = LiveBus(-20, -20)
        bus3 = LiveBus(100, 100)

        buses = [bus1, bus2, bus3]
        my_lat = 10.0
        my_lng = 10.0

        nearest = nearest_buses(buses, my_lat, my_lng, 2)
        self.assertEquals(nearest, [bus1, bus2])

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

    #########
    # forms #
    #########



