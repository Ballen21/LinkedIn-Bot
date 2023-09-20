import unittest
from unittest.mock import MagicMock
from bot import *


class TestLinkedInBot(unittest.TestCase):
    def setUp(self):
        # Mock the webdriver to avoid actual browser interaction
        self.bot = LinkedInBot("test@gmail.com", "testPassword")
        self.bot.driver = MagicMock()

    def tearDown(self):
        self.bot.driver = None

    def test_login_success(self):
        # Mock successful login by setting the current URL
        self.bot.driver.current_url = "https://www.linkedin.com/feed"
        self.bot.login()
        # Assert that no exceptions were raised, indicating successful login

    def test_login_failure(self):
        # Mock login failure by setting the current URL to a different page
        self.bot.driver.current_url = "https://www.linkedin.com/login"
        with self.assertRaises(Exception):
            self.bot.login()

    def test_add_school_connections_success(self):
        # Mock successful connection adding
        self.bot.driver.find_elements.return_value = [MagicMock()]*3
        self.bot.add_school_connections()
        # Assert that no exceptions were raised, indicating successful connection adding

    def test_add_school_connections_no_driver(self):
        self.bot.driver = None
        with self.assertRaises(Exception):
            self.bot.add_school_connections()

    def test_add_school_connections_failure(self):
        # Mock failure to find the "Connect" buttons
        self.bot.driver.find_elements.return_value = []
        with self.assertRaises(Exception):
            self.bot.add_school_connections()

if __name__ == '__main__':
    unittest.main()
