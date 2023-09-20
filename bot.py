import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import logging


class LinkedInBot:
    def __init__(self, email_param, password_param):
        self.email = email_param
        self.password = password_param
        self.driver = None
        self.wait = None
        self.logger = self.setup_logger()  # Initialize the logger

    @staticmethod
    def setup_logger():
        # Create a logger for logging errors
        logger = logging.getLogger("LinkedInBot")
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler = logging.FileHandler("linkedin_bot.log")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

    def login(self):
        try:
            self.driver = selenium.webdriver.Firefox()
            self.wait = WebDriverWait(self.driver, 10)
            self.driver.get("https://www.linkedin.com")

            # Locate email and password input fields, and login button
            email_input = self.wait.until(ec.presence_of_element_located((By.ID, "session_key")))
            password_input = self.driver.find_element(By.ID, "session_password")
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button.btn-md.btn-primary")

            # Click the login button using JavaScript to avoid potential issues
            self.driver.execute_script("arguments[0].click();", login_button)

            # Fill in email and password
            email_input.send_keys(self.email)
            password_input.send_keys(self.password)
            login_button.click()

            # Add error handling for login failures (e.g., invalid credentials)
            if "feed" not in self.driver.current_url:
                raise Exception("Login failed. Check your credentials.")

        except selenium.common.exceptions.TimeoutException:
            # Handle timeout exception (e.g., element not found within the timeout)
            self.logger.error("Timeout while waiting for an element.")
        except selenium.common.exceptions.WebDriverException as e:
            # Handle WebDriver exceptions (e.g., browser crashes)
            self.logger.error(f"WebDriverException: {str(e)}")
        except Exception as e:
            # Handle other exceptions
            self.logger.error(f"An error occurred: {str(e)}")

    def add_school_connections(self):
        try:
            if not self.driver:
                self.logger.error("WebDriver is not initialized.")
                return

            self.driver.get("https://www.linkedin.com/mynetwork/")

            # Scroll down the page to load more suggested connections
            for _ in range(3):
                self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
                time.sleep(2)

            # Find and click the "Connect" buttons for suggested connections
            connect_buttons = self.driver.find_elements(By.XPATH, "//button[text()='Connect']")
            for button in connect_buttons:
                button.click()
                time.sleep(2)

        except selenium.common.exceptions.NoSuchElementException:
            # Handle element not found exception
            self.logger.error("Element not found while adding connections.")
        except Exception as e:
            # Handle other exceptions
            self.logger.error(f"An error occurred: {str(e)}")

    def close(self):
        if self.driver:
            self.driver.quit()


if __name__ == "__main__":
    email = "your.email@gmail.com"  # fill in with your email
    password = "yourPassword"  # fill in with your password

    bot = LinkedInBot(email, password)
    try:
        bot.login()
        bot.add_school_connections()
    finally:
        bot.close()
