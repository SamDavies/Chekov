from django.test import TestCase
from selenium import webdriver

__author__ = 'Sam Davies'


class BusFinderTest(TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_add_services(self):
        self.driver.get("http://localhost:8000/?lat=55.9443730&lng=-3.1868930")
        # find the list of buttons

        # click 2

        # check that those 2 are displayed

        # check that the others are not

        available_buttons = self.driver.find_element_by_id('available-routes').find_elements_by_class_name('btn')
        for btn in available_buttons:
            btn.click()
        self.assertIn("http://localhost:8000/", self.driver.current_url)

    def test_remove_services(self):
        pass

    def tearDown(self):
        self.driver.quit()