from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

import time
import os

MAX_WAIT = 3

class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(by=By.ID, value='id_list_table')
                rows = table.find_elements(by=By.TAG_NAME, value='tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_layout_and_styling(self):
        # she opens the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # everything is neatly centere
        inputbox = self.browser.find_element(by=By.ID, value='id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta = 10
        )
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element(by=By.ID, value='id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta = 10
        )


    def test_can_start_a_list_for_one_user(self):
        self.browser.get(self.live_server_url)

        # To-Do app homepage exists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element(by=By.TAG_NAME, value='h1').text
        self.assertIn('To-Do', header_text)
        
        # user is given an option to add a to-do item into a text field
        inputbox = self.browser.find_element(by=By.ID, value='id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # user types in an item
        inputbox.send_keys('Buy feathers')

        # user confirms an input, page updates
        inputbox.send_keys(Keys.ENTER)

        # new element appears on the page
        self.wait_for_row_in_list_table('1: Buy feathers')

        # user performs another input
        inputbox = self.browser.find_element(by=By.ID, value='id_new_item')
        inputbox.send_keys('Make a hat from feathers')
        inputbox.send_keys(Keys.ENTER)

        # yet another element appears on the page
        self.wait_for_row_in_list_table('1: Buy feathers')
        self.wait_for_row_in_list_table('2: Make a hat from feathers')

        # user visits the generated url, the list is in place
        self.browser.quit()

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith works with the website and enters a list item
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(by=By.ID, value='id_new_item')
        inputbox.send_keys('Buy feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy feathers')

        # a unique URL has been created for Edith's list
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # Francis enters the site
        ## we start a new browser to remove cookies etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the homepage, there are no trails of Edith
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(by=By.TAG_NAME, value='body').text
        self.assertNotIn('Buy feathers', page_text)
        self.assertNotIn('Make a hat', page_text)

        # Francis starts his own list
        inputbox = self.browser.find_element(by=By.ID, value='id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # a unique URL has been created for Francis' list
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # there are no trails of Edith's list
        page_text = self.browser.find_element(by=By.TAG_NAME, value='body').text
        self.assertNotIn('Buy feathers', page_text)
        self.assertIn('Buy milk', page_text)
