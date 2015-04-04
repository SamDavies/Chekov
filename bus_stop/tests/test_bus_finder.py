from django.test import TestCase
from selenium import webdriver

__author__ = 'Sam Davies'


class BusFinderTest(TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_add_remove_service(self):
        self.driver.get("http://localhost:8000/?lat=55.9443730&lng=-3.1868930")

        self.add_chosen_services()
        self.remove_chosen_services()

        self.assertIn("http://localhost:8000/", self.driver.current_url)

    def add_chosen_services(self):
        # find the list of buttons
        available_buttons, chosen_buttons = self.refresh_dom_buttons()

        # click the first button
        btn1 = available_buttons[0]
        btn1_text = btn1.text
        btn1.click()

        available_buttons, chosen_buttons = self.refresh_dom_buttons()

        # make sure that it has disappeared
        self.check_not_contains(available_buttons, btn1_text)

        # make sure that is is available
        self.check_contains(chosen_buttons, btn1_text)

    def check_contains(self, buttons, text):
        """check if the buttons array has a button containing the text"""
        contains_btn = False
        for btn in buttons:
            if btn.text == text:
                contains_btn = True
                break
        self.assertTrue(contains_btn)

    def check_not_contains(self, buttons, text):
        """make sure buttons array has NO button containing the text"""
        for btn in buttons:
            self.assertNotEquals(btn.text, text)

    def refresh_dom_buttons(self):
        available_buttons = self.driver.find_element_by_id('available-routes').find_elements_by_class_name('btn')
        chosen_buttons = self.driver.find_element_by_id('chosen-routes').find_elements_by_class_name('btn')
        return available_buttons, chosen_buttons

    def remove_chosen_services(self):
        pass

    def tearDown(self):
        self.driver.quit()