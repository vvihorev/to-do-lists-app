from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

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

    def test_can_start_a_list_and_retrieve_it_later(self):
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

        # a text explaining that a unique URL has been created appears on the page
        # user visits the generated url, the list is in place

        self.fail('Tests finished!')
        browser.quit()

