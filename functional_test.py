from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')

        # To-Do app homepage exists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)
        
        # user is given an option to add a to-do item into a text field
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # user types in an item
        inputbox.send_keys('Buy feathers')

        # user confirms an input, page updates
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # new element appears on the page
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_element_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy feathers' for row in rows)
        )

        # user performs another input
        # yet another element appears on the page
        # a text explaining that a unique URL has been created appears on the page
        # user visits the generated url, the list is in place

        self.fail('Tests finished!')
        browser.quit()


if __name__ == "__main__":
    unittest.main(warnings="ignore")
