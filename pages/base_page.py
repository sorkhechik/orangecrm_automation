from seleniumbase import BaseCase
import os
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, sb: BaseCase):
        self.sb = sb
        # logger به صورت مرکزی در conftest.py تنظیم می‌شود
        self.logger = self.sb.logger if hasattr(self.sb, 'logger') else BaseCase.logger

    def type_text(self, locator, text, test_name=None):
        self.logger.info(f"Typing '{text}' into {locator}")
        try:
            self.sb.type(locator, text)
        except WebDriverException as e:
            self.logger.error(f"Failed to type into {locator}: {str(e)}")
            if test_name:
                self.save_screenshot(f"{test_name}_type_error")
            raise

    def click_element(self, locator, test_name=None):
        self.logger.info(f"Clicking on {locator}")
        try:
            self.sb.click(locator)
        except WebDriverException as e:
            self.logger.error(f"Failed to click {locator}: {str(e)}")
            if test_name:
                self.save_screenshot(f"{test_name}_click_error")
            raise

    def wait_for_element(self, locator, timeout=30, test_name=None):
        self.logger.info(f"Waiting for element {locator}")
        try:
            self.sb.wait_for_element_visible(locator, timeout=timeout)
        except WebDriverException as e:
            self.logger.error(f"Failed to wait for {locator}: {str(e)}")
            if test_name:
                self.save_screenshot(f"{test_name}_wait_error")
            raise

    def assert_element_present(self, locator, timeout=30, test_name=None):
        self.logger.info(f"Asserting element {locator} is present")
        try:
            self.sb.assert_element_present(locator, timeout=timeout)
        except WebDriverException as e:
            self.logger.error(f"Element {locator} not found: {str(e)}")
            if test_name:
                self.save_screenshot(f"{test_name}_assert_error")
            raise

    def get_text(self, locator, test_name=None):
        self.logger.info(f"Getting text from {locator}")
        try:
            return self.sb.get_text(locator)
        except WebDriverException as e:
            self.logger.error(f"Failed to get text from {locator}: {str(e)}")
            if test_name:
                self.save_screenshot(f"{test_name}_get_text_error")
            raise

    def save_page_source(self, filename, test_name=None):
        self.logger.info(f"Saving page source to {filename}")
        os.makedirs("screenshots", exist_ok=True)
        try:
            full_filename = f"screenshots/{test_name}_{filename}_source.html" if test_name else f"screenshots/{filename}_source.html"
            with open(full_filename, "w", encoding="utf-8") as f:
                f.write(self.sb.get_page_source())
        except WebDriverException as e:
            self.logger.error(f"Failed to save page source: {str(e)}")
            if test_name:
                self.save_screenshot(f"{test_name}_source_error")

    def save_screenshot(self, filename, test_name=None):
        self.logger.info(f"Saving screenshot to {filename}")
        os.makedirs("screenshots", exist_ok=True)
        try:
            full_filename = f"screenshots/{test_name}_{filename}.png" if test_name else f"screenshots/{filename}.png"
            self.sb.save_screenshot(full_filename)
        except WebDriverException as e:
            self.logger.error(f"Failed to save screenshot: {str(e)}")



    # def is_element_visible(self, css_selector, by="css selector" , timeout=2):
    #     """
    #     Check if element is visible on the page.

    #     Args:
    #         css_selector (str): CSS locator.
    #         timeout (int): Timeout to wait.

    #     Returns:
    #         bool: True if visible, False otherwise.
    #     """
    #     try:
    #         WebDriverWait(self.sb.driver, timeout).until(
    #             EC.visibility_of_element_located((by, css_selector))
    #         )
    #         return True
    #     except Exception:
    #         return False
