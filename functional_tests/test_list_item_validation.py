from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # Edith opens the homepage and tries to send an empty list element.
        # She presses enter on an empty input field

        # The homepage refreshes, an error message appears: "List elements should not be empty"

        # She inputs some text and tries again, it works.

        # She tries to send an empty element one more time, the error is shown.
        self.fail('write me!')
