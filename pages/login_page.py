from pages.base_page import BasePage
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import os
import pytest

class LoginPage(BasePage):
    USERNAME_FIELD = "input[name='username']"
    PASSWORD_FIELD = "input[name='password']"
    LOGIN_BUTTON = "button[type='submit']"
    ERROR_MESSAGE = "div.oxd-alert-content-text"
    DASHBOARD_HEADER = "h6.oxd-topbar-header-breadcrumb-module"

    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_WAIT", 30))

    def login(self, username, password, test_name=None):
        self.logger.info(f"Starting login process for user: {username}")

        try:
            self.logger.info("Waiting for login page to load")
            self.wait_for_element(self.USERNAME_FIELD, timeout=self.DEFAULT_TIMEOUT, test_name=test_name)
            self.save_screenshot("login_page_loaded", test_name=test_name)
            self.save_page_source("login_page_loaded", test_name=test_name)

            self.logger.info("Entering username")
            self.type_text(self.USERNAME_FIELD, username, test_name=test_name)

            self.logger.info("Entering password")
            self.type_text(self.PASSWORD_FIELD, password, test_name=test_name)  # Do NOT log actual password

            self.logger.info("Clicking login button")
            self.click_element(self.LOGIN_BUTTON, test_name=test_name)

            self.logger.info("Waiting for either error message or dashboard header")
            if self._wait_for_login_result(max_wait=self.DEFAULT_TIMEOUT * 2, test_name=test_name):
                self.logger.info("Login successful, dashboard loaded")
                self.save_screenshot("login_success", test_name=test_name)
                self.save_page_source("login_success", test_name=test_name)
            else:
                error_message = self.get_text(self.ERROR_MESSAGE, test_name=test_name)
                self.logger.error(f"Login failed: {error_message}")
                raise AssertionError(f"Login failed: {error_message}")

            self.save_screenshot("login_attempt", test_name=test_name)
            self.save_page_source("login_attempt", test_name=test_name)

        except TimeoutException as e:
            self.logger.error(f"Login timed out: {str(e)}")
            self.save_screenshot("login_timeout", test_name=test_name)
            self.save_page_source("login_timeout", test_name=test_name)
            raise
        except Exception as e:
            self.logger.error(f"Login process failed: {str(e)}")
            self.save_screenshot("login_error", test_name=test_name)
            self.save_page_source("login_error", test_name=test_name)
            raise

    def _wait_for_login_result(self, max_wait=None, test_name=None):
        """
        Waits for either the dashboard or error message to appear.
        Args:
            max_wait (int, optional): Maximum wait time in seconds. Defaults to DEFAULT_TIMEOUT * 2.
            test_name (str, optional): Name of the test for screenshot naming.
        Returns:
            True if dashboard appears (login successful), False if error message found.
        """
        max_wait = max_wait if max_wait is not None else self.DEFAULT_TIMEOUT * 2
        try:
            for _ in range(int(max_wait / 0.5)):
                if self.is_element_visible(self.DASHBOARD_HEADER, test_name=test_name):
                    return True
                if self.is_element_visible(self.ERROR_MESSAGE, test_name=test_name):
                    return False
                self.sb.sleep(0.5)
            raise TimeoutException(f"Neither dashboard nor error message appeared within {max_wait} seconds.")
        except Exception as e:
            self.logger.error(f"Unexpected error during login result check: {type(e).__name__} - {str(e)}")
            self.save_screenshot("login_result_error", test_name=test_name)
            raise

    def get_error_message(self, test_name=None):
        """
        Returns the login error message text if present, or None.
        """
        try:
            if self.is_element_visible(self.ERROR_MESSAGE, test_name=test_name):
                return self.get_text(self.ERROR_MESSAGE, test_name=test_name)
            return None
        except Exception as e:
            self.logger.error(f"Failed to get error message: {str(e)}")
            self.save_screenshot("error_message_error", test_name=test_name)
            return None