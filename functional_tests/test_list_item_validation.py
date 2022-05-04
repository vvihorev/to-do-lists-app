from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # Edith opens the homepage and tries to send an empty list element.
        # She presses enter on an empty input field
        self.browser.get(self.live_server_url)
        self.browser.find_element(by=By.ID, value="id_new_item").send_keys(Keys.ENTER)

        # The homepage refreshes, an error message appears: "List elements should not be empty"
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item"
        ))

        # She inputs some text and tries again, it works.
        self.browser.find_element(by=By.ID, value="id_new_item").send_keys("Buy milk")
        self.browser.find_element(by=By.ID, value="id_new_item").send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk [x]")

        # She tries to send an empty element one more time, the error is shown.
        self.browser.find_element(by=By.ID, value="id_new_item").send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item"
        ))
        self.browser.find_element(by=By.ID, value="id_new_item").send_keys("Make tea")
        self.browser.find_element(by=By.ID, value="id_new_item").send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy milk [x]")
        self.wait_for_row_in_list_table("2: Make tea [x]")
