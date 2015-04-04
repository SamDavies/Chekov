from django.test import TestCase
from selenium import webdriver

__author__ = 'Sam Davies'


class BusFinderTest(TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_add_services(self):
        self.driver.get("http://localhost:8000/?lat=55.9443730&lng=-3.1868930")

        # find the list of buttons
        available_buttons, chosen_buttons = self.refresh_dom_buttons()

        # click the first button
        btn1 = available_buttons[0]
        btn1_text = btn1.text
        btn1.click()

        available_buttons, chosen_buttons = self.refresh_dom_buttons()

        # make sure that it has disappeared
        for btn in available_buttons:
            self.assertNotEquals(btn.text, btn1_text)

        # make sure that is is available
        contains_btn = False
        for btn in chosen_buttons:
            if btn.text == btn1_text:
                contains_btn = True
                break
        self.assertTrue(contains_btn)

        self.assertIn("http://localhost:8000/", self.driver.current_url)

    def refresh_dom_buttons(self):
        available_buttons = self.driver.find_element_by_id('available-routes').find_elements_by_class_name('btn')
        chosen_buttons = self.driver.find_element_by_id('chosen-routes').find_elements_by_class_name('btn')
        return available_buttons, chosen_buttons

    def test_remove_services(self):
        pass

    def tearDown(self):
        self.driver.quit()