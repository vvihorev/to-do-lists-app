from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):

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
        self.wait_for_row_in_list_table('1: Buy feathers [x]')

        # user performs another input
        inputbox = self.browser.find_element(by=By.ID, value='id_new_item')
        inputbox.send_keys('Make a hat from feathers')
        inputbox.send_keys(Keys.ENTER)

        # yet another element appears on the page
        self.wait_for_row_in_list_table('1: Buy feathers [x]')
        self.wait_for_row_in_list_table('2: Make a hat from feathers [x]')

        # user visits the generated url, the list is in place
        self.browser.quit()

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith works with the website and enters a list item
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(by=By.ID, value='id_new_item')
        inputbox.send_keys('Buy feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy feathers [x]')

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
        self.wait_for_row_in_list_table('1: Buy milk [x]')

        # a unique URL has been created for Francis' list
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # there are no trails of Edith's list
        page_text = self.browser.find_element(by=By.TAG_NAME, value='body').text
        self.assertNotIn('Buy feathers', page_text)
        self.assertIn('Buy milk', page_text)

