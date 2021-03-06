import datetime
import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from app.views import nearest_to_me, next_stop, is_after_current_time, get_stop, next_stops, get_previous_and_next


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

        return nearest_to_me(buses, my_lat, my_lng, x), bus1, bus2, bus3

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

    def test_after_current_time(self):
        """ensure that future time is found"""
        check_time_str = self.get_time_string(1)
        self.assertTrue(is_after_current_time(check_time_str))

    def test_before_current_time(self):
        """ensure that past time is found"""
        check_time_str = self.get_time_string(-1)
        self.assertFalse(is_after_current_time(check_time_str))

    def test_get_stop(self):
        """ensure that a stop can be fetched from its id"""
        stop1 = dict(stop_id="hello")
        stop2 = dict(stop_id="my")
        stop3 = dict(stop_id="son")
        stops = [stop1, stop2, stop3]
        stop = get_stop("my", stops)
        self.assertEquals(stop, stop2)

    def test_next_stops(self):
        """ensure that all the next stops for the journeys are """
        stop1 = dict(stop_id="hello", other="other1")
        stop2 = dict(stop_id="my", other="other2")
        stop3 = dict(stop_id="son", other="other3")
        stops = [stop1, stop2, stop3]

        departures1 = dict(time=self.get_time_string(-1), stop_id="hello")
        departures2 = dict(time=self.get_time_string(10), stop_id="my")
        departures3 = dict(time=self.get_time_string(100), stop_id="son")

        journeys = [dict(departures=[departures1, departures2, departures3])]

        result = next_stops(journeys, stops)
        self.assertEquals(len(result), 2)
        self.assertEquals(result[0][0]['other'], "other2")
        self.assertDictEqual(result[1][0], journeys[0])

    def get_time_string(self, offset):
        hours, mins = datetime.datetime.now().hour, datetime.datetime.now().minute
        return "{0}:{1}".format(str(hours + 1), str(mins+offset))

    def test_get_previous_and_next(self):
        journey = dict(departures=[dict(stop_id=95624796), dict(stop_id=36234956), dict(stop_id=36234959),
                                   dict(stop_id=36234945), dict(stop_id=36234939), dict(stop_id=36237546)])
        stop = dict(stop_id=36234959)
        three_stops = get_previous_and_next(stop, journey)
        expected = [dict(name='Main Street', stop_id=36234956), dict(name='Bavelaw Road', stop_id=36234959),
                    dict(name='Bavelaw Rd bridge', stop_id=36234945)]
        self.assertEquals(three_stops, expected)

    def test_get_previous_and_next_first(self):
        journey = dict(departures=[dict(stop_id=95624796), dict(stop_id=36234956), dict(stop_id=36234959),
                                   dict(stop_id=36234945), dict(stop_id=36234939), dict(stop_id=36237546)])
        stop = dict(stop_id=95624796)
        three_stops = get_previous_and_next(stop, journey)
        expected = [dict(name='Deans South', stop_id=95624796), dict(name='Main Street', stop_id=36234956)]
        self.assertEquals(three_stops, expected)

    def test_get_previous_and_next_last(self):
        journey = dict(departures=[dict(stop_id=95624796), dict(stop_id=36234956), dict(stop_id=36234959),
                                   dict(stop_id=36234945), dict(stop_id=36234939), dict(stop_id=36237546)])
        stop = dict(stop_id=36237546)
        three_stops = get_previous_and_next(stop, journey)
        expected = [dict(name='Lanark Road West', stop_id=36234939), dict(name='Newmills Road', stop_id=36237546)]
        self.assertEquals(three_stops, expected)

    ##########
    # models #
    ##########

    ########################
    # views (uses reverse) #
    ########################

    def test_home_load(self):
        """ensure that the home page loads"""
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_stops_load(self):
        """ensure that the stops page loads"""
        response = self.client.get(reverse("stops"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Deans South', response.content)

    def test_live_buses_load(self):
        """ensure that the live buses page loads"""
        response = self.client.get(reverse("live_buses"), data=dict(lat='55.9443730', lng='-3.1868930'))
        self.assertEqual(response.status_code, 200)

    def test_get_feed(self):
        """ensure that the feed page loads"""
        data = dict(lat='55.944373', lng='-3.186893', service='3', destination="Clovenstone Drive")
        r = self.client.get(reverse("get_feed"), data=data)
        self.assertEqual(r.status_code, 200)

    def test_tracker(self):
        """ensure that the tracker page loads"""
        data = dict(lat='55.944373', lng='-3.186893', service='3', destination="Clovenstone Drive")
        r = self.client.get(reverse("tracker"), data=data)
        self.assertEqual(r.status_code, 200)

    def test_tracker_data(self):
        """ensure that the tracker page loads"""
        data = dict(lat='55.944373', lng='-3.186893', service='3', destination="Clovenstone Drive")
        r = self.client.get(reverse("tracker_data"), data=data)
        self.assertEqual(r.status_code, 200)

    #########
    # forms #
    #########