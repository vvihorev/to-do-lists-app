from selenium import webdriver
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
        self.fail('Tests finished!')
        
        # user inputs item into a text field
        # new element appears on the page
        # user performs another input
        # new element appears on the page
        # a text explaining that a unique URL has been created appears on the page
        # user visits the generated url, the list is in place

        browser.quit()


if __name__ == "__main__":
    unittest.main(warnings="ignore")
